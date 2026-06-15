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
class Grade3CreateBookFlowTest {

    @Autowired MockMvc mockMvc;
    @Autowired LibraryStore store;

    @BeforeEach
    void setup() {
        store.resetWithSampleData();
    }

    @Test
    @DisplayName("3.0: POST /books tworzy książkę i robi redirect do /books")
    void shouldCreateBookAndRedirect() throws Exception {
        mockMvc.perform(post("/books")
                        .param("title", "Domain-Driven Design")
                        .param("author", "Eric Evans")
                        .param("totalCopies", "3"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/books"));

        assertEquals(4, store.getBooks().size());
        assertTrue(store.getBooks().stream().anyMatch(book ->
                book.getTitle().equals("Domain-Driven Design")
                        && book.getAuthor().equals("Eric Evans")
                        && book.getTotalCopies() == 3
                        && book.getAvailableCopies() == 3));
    }
}
