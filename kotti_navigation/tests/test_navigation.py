from pyramid.threadlocal import get_current_registry
from kotti.testing import (
    FunctionalTestBase,
    DummyRequest,
)
from kotti.resources import (
        get_root,
        Content,
)
from kotti.views.util import render_view
from kotti_navigation.views import navigation_widget


class NavigationDummyRequest(DummyRequest):

    def __init__(self, context=None):
        super(NavigationDummyRequest, self).__init__()
        self.context = context

    def static_url(self, name):
        return ''  # pragma: no cover


class TestNavigationWidgetAsHorizontal(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'pyramid.includes': 'kotti_navigation.include_navigation_widget_left',
                    'kotti_navigation.navigation_widget.display_type': 'horizontal',
                    'kotti_navigation.navigation_widget.show_dropdown_menus': 'false',
                    'kotti_navigation.navigation_widget.label': 'context'}
        super(TestNavigationWidgetAsHorizontal, self).setUp(**settings)

    def test_render_widget(self):
        root = get_root()
        html = render_view(root, NavigationDummyRequest(), name='navigation-widget')
        # Note trailing blank after nav-pills, there because nav-stacked is
        # conditionally removed in the template.
        assert '<ul class="nav nav-pills ">' in html

    def test_show_dropdown_menus(self):
        request = NavigationDummyRequest()
        root = get_root()
        result = navigation_widget(root, request)
        assert result['show_dropdown_menus'] == False

        root[u'content_1'] = Content(title=u'Content_1')
        root[u'content_1'][u'sub_1'] = Content(title=u'Sub_1')
        root[u'content_1'][u'sub_1'][u'sub_sub_1'] = Content(title=u'Sub_Sub_1')
        root[u'content_2'] = Content(title=u'Content_2')
        root[u'content_2'][u'sub_2'] = Content(title=u'Sub_2')

        html = render_view(root[u'content_1'], NavigationDummyRequest(), name='navigation-widget')

        assert not u'nav-list-careted' in html

        get_current_registry().settings['kotti_navigation.navigation_widget.show_dropdown_menus'] = u'true'

        html = render_view(root[u'content_1'], NavigationDummyRequest(), name='navigation-widget')

        assert u'nav-list-careted' in html

    def test_label(self):
        request = NavigationDummyRequest()
        root = get_root()

        root[u'content_1'] = Content(title=u'Content_1')
        root[u'content_1'][u'sub_1'] = Content(title=u'Sub_1')
        root[u'content_2'] = Content(title=u'Content_2')
        root[u'content_2'][u'sub_2'] = Content(title=u'Sub_2')

        result = navigation_widget(root, request)

        assert result['before_context'] == ''
        assert result['after_context'] == ''
        assert result['items'][0].title == 'Content_1'

        get_current_registry().settings['kotti_navigation.navigation_widget.label'] = u'Items in [context] are:'
        result = navigation_widget(root[u'content_1'], request)
        assert result['before_context'] == 'Items in ['
        assert result['items'][0].title == 'Content_1'
        assert result['after_context'] == '] are:'


class TestNavigationWidgetAsTree(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'pyramid.includes': 'kotti_navigation.include_navigation_widget_left',
                    'kotti_navigation.navigation_widget.include_root': 'true',
                    'kotti_navigation.navigation_widget.display_type': 'tree',
                    'kotti_navigation.navigation_widget.open_all': 'false'}
        super(TestNavigationWidgetAsTree, self).setUp(**settings)

    def test_render_widget(self):
        root = get_root()
        html = render_view(root, NavigationDummyRequest(), name='navigation-widget')
        assert '<ul class="nav nav-pills nav-stacked">' in html

    def test_include_root(self):
        request = NavigationDummyRequest()
        root = get_root()
        result = navigation_widget(root, request)
        assert result['include_root'] == True
        get_current_registry().settings['kotti_navigation.navigation_widget.include_root'] = u'false'
        result = navigation_widget(root, request)
        assert result['include_root'] == False

    def test_display_type(self):
        request = NavigationDummyRequest()
        root = get_root()
        result = navigation_widget(root, request)
        assert result['display_type'] == 'tree'
        get_current_registry().settings['kotti_navigation.navigation_widget.display_type'] = u'horizontal'
        result = navigation_widget(root, request)
        assert result['display_type'] == 'horizontal'

    def test_is_tree_open(self):
        request = NavigationDummyRequest()
        root = get_root()
        root[u'content_1'] = Content()
        root[u'content_1'][u'sub_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'][u'sub_2'] = Content()

        request.context = root
        html = render_view(root, request, name='navigation-widget')
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' not in html

        request.context = root[u'content_1']
        html = render_view(root[u'content_1'], request, name='navigation-widget')
        assert u'content_1' in html
        assert u'sub_1' in html
        assert u'content_2' in html
        assert u'sub_2' not in html

        request.context = root[u'content_2']
        html = render_view(root[u'content_2'], request, name='navigation-widget')
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' in html

        request.context = root[u'content_2'][u'sub_2']
        html = render_view(root[u'content_2'][u'sub_2'], request, name='navigation-widget')
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' in html

        get_current_registry().settings['kotti_navigation.navigation_widget.open_all'] = u'true'
        request.context = root
        html = render_view(root, request, name='navigation-widget')
        assert u'content_1' in html
        assert u'sub_1' in html
        assert u'content_2' in html
        assert u'sub_2' in html

    def test_show_hidden(self):
        root = get_root()
        request = DummyRequest()
        root[u'content_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'].in_navigation = False

        # with standard settings the hidden nav points are hidden
        html = render_view(root, request, name='navigation-widget')
        assert u'content_1' in html
        assert u'content_2' not in html

        # if we change the setting, the nav points still hidden
        get_current_registry().settings['kotti_navigation.navigation_widget.show_hidden_while_logged_in'] = u'true'
        html = render_view(root, request, name='navigation-widget')
        assert u'content_1' in html
        assert u'content_2' not in html

        # we have to be logged in to see the navpoint
        # BUT how is this possible???
        # from kotti.views.login import login
        # request.params['submit'] = u'on'
        # request.params['login'] = u'admin'
        # request.params['password'] = u'secret'
        # request.params['HTTP_HOST'] = u'babbelhorst.net'
        # result = self.login()
        # html = render_navigation_widget(root, request)
        # assert u'content_1' in html
        # assert u'content_2' in html

    def test_exclude_content_types(self):
        root = get_root()
        request = DummyRequest()
        root[u'content_1'] = Content()

        # with no exclude the hidden nav points is shown
        html = render_view(root, request, name='navigation-widget')
        assert u'content_1' in html

        # if we exclude the content type the nav point disappears
        get_current_registry().settings['kotti_navigation.navigation_widget.exclude_content_types'] = u'kotti.resources.Content'
        html = render_view(root, request, name='navigation-widget')
        assert u'content_1' not in html
