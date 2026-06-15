package pl.example.lab6;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.web.servlet.MockMvc;
import pl.example.lab6.store.LibraryStore;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@Import(TestClockConfig.class)
class Grade3LoanAvailabilityTest {

    @Autowired
    MockMvc mockMvc;
    @Autowired
    LibraryStore store;

    @BeforeEach
    void setup() {
        store.resetWithSampleData();
        store.getBook(3L).setAvailableCopies(0);
    }

    @Test
    @DisplayName("3.0: Brak egzemplarzy zwraca formularz z błędem i nie tworzy wypożyczenia")
    void shouldReturnFormWithGlobalErrorWhenNoCopiesAvailable() throws Exception {
        mockMvc.perform(post("/loans")
                .param("bookId", "3")
                .param("borrower", "Anna"))
                .andExpect(status().isOk())
                .andExpect(view().name("loans/form"))
                .andExpect(model().attributeHasErrors("loanForm"))
                .andExpect(content().string(org.hamcrest.Matchers.containsString("No copies available")));

        assertEquals(0, store.getLoans().size());
        assertEquals(0, store.getBook(3L).getAvailableCopies());
    }
}
