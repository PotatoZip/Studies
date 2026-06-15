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

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@Import(TestClockConfig.class)
class Grade3LoanFormPageTest {

    @Autowired MockMvc mockMvc;
    @Autowired LibraryStore store;

    @BeforeEach
    void setup() {
        store.resetWithSampleData();
    }

    @Test
    @DisplayName("3.0: GET /loans/new renderuje formularz wypożyczenia dla wybranej książki")
    void shouldRenderLoanFormForSelectedBook() throws Exception {
        mockMvc.perform(get("/loans/new").param("bookId", "1"))
                .andExpect(status().isOk())
                .andExpect(view().name("loans/form"))
                .andExpect(model().attributeExists("loanForm"))
                .andExpect(model().attributeExists("selectedBook"))
                .andExpect(content().string(org.hamcrest.Matchers.containsString("Clean Code")));
    }
}
