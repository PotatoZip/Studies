package pl.example.lab6.service;

import org.springframework.stereotype.Service;
import pl.example.lab6.dto.BookForm;
import pl.example.lab6.dto.LoanForm;
import pl.example.lab6.model.Book;
import pl.example.lab6.model.Loan;
import pl.example.lab6.store.LibraryStore;
import pl.example.lab6.view.BookListItem;
import pl.example.lab6.view.DashboardView;
import pl.example.lab6.view.LoanListItem;

import java.time.Clock;
import java.time.LocalDate;
import java.util.List;
import java.util.NoSuchElementException;

@Service
public class LibraryServiceImpl implements LibraryService {

    private final LibraryStore store;
    private final LibraryViewMapper mapper;
    private final Clock clock;

    public LibraryServiceImpl(LibraryStore store, LibraryViewMapper mapper, Clock clock) {
        this.store = store;
        this.mapper = mapper;
        this.clock = clock;
    }

    @Override
    public List<BookListItem> getBooks() {
        return store.getBooks().stream()
                .sorted((left, right) -> Long.compare(left.getId(), right.getId()))
                .map(mapper::toBookListItem)
                .toList();
    }

    @Override
    public Book createBook(BookForm form) {
        Book book = new Book();
        book.setId(store.nextBookId());
        book.setTitle(form.getTitle());
        book.setAuthor(form.getAuthor());
        book.setTotalCopies(form.getTotalCopies());
        book.setAvailableCopies(form.getTotalCopies());
        return store.saveBook(book);
    }

    @Override
    public Book getBook(long bookId) {
        Book book = store.getBook(bookId);
        if (book == null) {
            throw new NoSuchElementException("Book not found: " + bookId);
        }
        return book;
    }

    @Override
    public void createLoan(LoanForm form) {
        Book book = getBook(form.getBookId());
        if (book.getAvailableCopies() <= 0) {
            throw new IllegalStateException("No copies available");
        }

        LocalDate borrowedOn = LocalDate.now(clock);
        Loan loan = new Loan();
        loan.setId(store.nextLoanId());
        loan.setBookId(book.getId());
        loan.setBorrower(form.getBorrower());
        loan.setBorrowedOn(borrowedOn);
        loan.setDueDate(borrowedOn.plusDays(14));
        loan.setReturned(false);

        book.setAvailableCopies(book.getAvailableCopies() - 1);
        store.saveLoan(loan);
        store.saveBook(book);
    }

    @Override
    public List<LoanListItem> getLoans(boolean activeOnly) {
        return store.getLoans().stream()
                .filter(loan -> !activeOnly || !loan.isReturned())
                .sorted((left, right) -> Long.compare(left.getId(), right.getId()))
                .map(loan -> mapper.toLoanListItem(loan, getBook(loan.getBookId())))
                .toList();
    }

    @Override
    public void returnLoan(long loanId) {
        Loan loan = store.getLoan(loanId);
        if (loan == null) {
            throw new NoSuchElementException("Loan not found: " + loanId);
        }
        if (!loan.isReturned()) {
            loan.setReturned(true);
            Book book = getBook(loan.getBookId());
            book.setAvailableCopies(book.getAvailableCopies() + 1);
            store.saveLoan(loan);
            store.saveBook(book);
        }
    }

    @Override
    public DashboardView getDashboard() {
        List<Book> books = store.getBooks();
        int booksCount = books.size();
        int totalCopies = books.stream().mapToInt(Book::getTotalCopies).sum();
        int availableCopies = books.stream().mapToInt(Book::getAvailableCopies).sum();
        int activeLoans = (int) store.getLoans().stream().filter(loan -> !loan.isReturned()).count();
        return new DashboardView(booksCount, totalCopies, availableCopies, activeLoans);
    }
}
