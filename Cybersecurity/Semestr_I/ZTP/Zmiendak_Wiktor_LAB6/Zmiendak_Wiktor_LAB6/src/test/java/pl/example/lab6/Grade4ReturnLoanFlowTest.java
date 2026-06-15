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
class Grade4ReturnLoanFlowTest {

    @Autowired MockMvc mockMvc;
    @Autowired LibraryStore store;

    @BeforeEach
    void setup() throws Exception {
        store.resetWithSampleData();
        mockMvc.perform(post("/loans")
                .param("bookId", "1")
                .param("borrower", "Jan"));
    }

    @Test
    @DisplayName("4.0: POST /loans/{id}/return oznacza wypożyczenie jako zwrócone i zwiększa stan")
    void shouldReturnLoanAndIncreaseAvailableCopies() throws Exception {
        mockMvc.perform(post("/loans/1/return"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/loans"));

        assertTrue(store.getLoan(1L).isReturned());
        assertEquals(4, store.getBook(1L).getAvailableCopies());
    }
}
