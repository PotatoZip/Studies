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
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@Import(TestClockConfig.class)
class Grade3CreateLoanFlowTest {

    @Autowired MockMvc mockMvc;
    @Autowired LibraryStore store;

    @BeforeEach
    void setup() {
        store.resetWithSampleData();
    }

    @Test
    @DisplayName("3.0: POST /loans tworzy wypożyczenie i zmniejsza liczbę dostępnych egzemplarzy")
    void shouldCreateLoanAndDecreaseAvailableCopies() throws Exception {
        mockMvc.perform(post("/loans")
                        .param("bookId", "1")
                        .param("borrower", "Jan Kowalski"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/loans"));

        assertEquals(1, store.getLoans().size());
        assertTrue(store.getLoans().stream().anyMatch(loan -> loan.getBorrower().equals("Jan Kowalski")));
        assertEquals(3, store.getBook(1L).getAvailableCopies());
    }
}
