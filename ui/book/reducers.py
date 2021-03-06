from .. import utility


class BookReducers():
    def go_to_start(self, state, value):
        return self.go_to_page(state, 0)

    def skip_pages(self, state, value):
        book_n = state['book']
        book = state['books'][book_n]
        page = book.page + value
        return self.go_to_page(state, page)

    def go_to_page(self, state, value):
        width, height = utility.dimensions(state)
        book_n = state['book']
        book = state['books'][book_n]
        page = value
        books = list(state['books'])
        books[book_n].page = utility.set_page(book, page, height)
        return state.copy(books=tuple(books),
                          location='book', home_menu_visible=False)

    def enter_go_to_page(self, state, value):
        return state.copy(home_menu_visible=False, location='go_to_page')

    def toggle_home_menu(self, state, value):
        return state.copy(home_menu_visible=not state['home_menu_visible'])
