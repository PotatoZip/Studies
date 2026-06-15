package pl.example.lab6.store;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;
import pl.example.lab6.model.Book;
import pl.example.lab6.model.Loan;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

@Component
public class LibraryStore {

    private final Map<Long, Book> books = new LinkedHashMap<>();
    private final Map<Long, Loan> loans = new LinkedHashMap<>();
    private final AtomicLong nextBookId = new AtomicLong();
    private final AtomicLong nextLoanId = new AtomicLong();

    @PostConstruct
    public void init() {
        resetWithSampleData();
    }

    public synchronized void resetWithSampleData() {
        books.clear();
        loans.clear();
        nextBookId.set(0);
        nextLoanId.set(0);

        saveBook(new Book(nextBookId(), "Clean Code", "Robert C. Martin", 4, 4));
        saveBook(new Book(nextBookId(), "Effective Java", "Joshua Bloch", 2, 2));
        saveBook(new Book(nextBookId(), "Refactoring", "Martin Fowler", 1, 1));
    }

    public synchronized long nextBookId() {
        return nextBookId.incrementAndGet();
    }

    public synchronized long nextLoanId() {
        return nextLoanId.incrementAndGet();
    }

    public synchronized List<Book> getBooks() {
        return new ArrayList<>(books.values());
    }

    public synchronized List<Loan> getLoans() {
        return new ArrayList<>(loans.values());
    }

    public synchronized Book getBook(Long id) {
        return books.get(id);
    }

    public synchronized Loan getLoan(Long id) {
        return loans.get(id);
    }

    public synchronized Book saveBook(Book book) {
        books.put(book.getId(), book);
        return book;
    }

    public synchronized Loan saveLoan(Loan loan) {
        loans.put(loan.getId(), loan);
        return loan;
    }
}
