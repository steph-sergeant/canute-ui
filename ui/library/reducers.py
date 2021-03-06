from frozendict import frozendict
import logging
from functools import partial

from .. import utility


log = logging.getLogger(__name__)


class LibraryReducers():
    def go_to_book(self, state, number):
        width, height = utility.dimensions(state)
        page = state['library']['page']
        line_number = page * (height - 1)
        try:
            state['books'][line_number + number]
        except:
            log.warning('no book at {}'.format(number))
            return state
        return state.copy(location='book', book=line_number + number,
                          home_menu_visible=False)

    def set_books(self, state, books):
        width, height = utility.dimensions(state)
        books = tuple(sort_books(books))
        data = list(map(lambda b: utility.to_braille(b.title), books))
        data = list(map(partial(utility.pad_line, width), data))
        library = frozendict({'data': tuple(data), 'page': 0})
        return state.copy(location='library', books=books, library=library)

    def add_books(self, state, books_to_add):
        width, height = utility.dimensions(state)
        book_filenames = [b.filename for b in state['books']]
        books_to_add = [
            d for d in books_to_add if d.filename not in book_filenames
        ]
        books = list(state['books'])
        books += list(books_to_add)
        books = sort_books(books)
        data = list(map(lambda b: utility.to_braille(b.title), books))
        data = list(map(partial(utility.pad_line, width), data))
        library = frozendict({
            'data': tuple(data),
            'page': state['library']['page']
        })
        return state.copy(books=tuple(books), library=library)

    def remove_books(self, state, filenames):
        width, height = utility.dimensions(state)
        books = [
            b for b in state['books'] if b.filename not in filenames
        ]
        data = list(map(lambda b: utility.to_braille(b.title), books))
        data = list(map(partial(utility.pad_line, width), data))
        maximum = utility.get_max_pages(data, height)
        page = state['library']['page']
        if page > maximum:
            page = maximum
        library = frozendict({'data': data, 'page': page})
        return state.copy(books=tuple(books), library=library)

    def replace_library(self, state, value):
        if state['replacing_library'] == 'in progress' and value != 'done':
            return state
        else:
            return state.copy(replacing_library=value, location='library')


def sort_books(books):
    return sorted(books, key=lambda book: book.title)
