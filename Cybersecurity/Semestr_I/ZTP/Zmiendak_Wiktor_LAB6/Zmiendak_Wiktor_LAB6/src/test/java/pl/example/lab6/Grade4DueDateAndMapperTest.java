package pl.example.lab6;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab6.dto.LoanForm;
import pl.example.lab6.service.LibraryServiceImpl;
import pl.example.lab6.service.LibraryViewMapper;
import pl.example.lab6.store.LibraryStore;
import pl.example.lab6.view.LoanListItem;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

class Grade4DueDateAndMapperTest {

    @Test
    @DisplayName("4.0: dueDate = borrowedOn + 14 dni i trafia do modelu widoku")
    void shouldCalculateDueDateAndExposeItInViewModel() {
        LibraryStore store = new LibraryStore();
        store.resetWithSampleData();
        LibraryViewMapper mapper = new LibraryViewMapper();
        Clock fixedClock = Clock.fixed(Instant.parse("2026-04-20T10:15:30Z"), ZoneOffset.UTC);
        LibraryServiceImpl service = new LibraryServiceImpl(store, mapper, fixedClock);

        service.createLoan(new LoanForm(1L, "Jan"));

        LoanListItem item = service.getLoans(false).get(0);
        assertEquals(java.time.LocalDate.parse("2026-04-20"), item.borrowedOn());
        assertEquals(java.time.LocalDate.parse("2026-05-04"), item.dueDate());
        assertFalse(item.returned());
        assertEquals("Clean Code", item.bookTitle());
    }
}
