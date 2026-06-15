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

import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@Import(TestClockConfig.class)
class Grade4ActiveLoansFilterTest {

    @Autowired MockMvc mockMvc;
    @Autowired LibraryStore store;

    @BeforeEach
    void setup() throws Exception {
        store.resetWithSampleData();
        mockMvc.perform(post("/loans").param("bookId", "1").param("borrower", "Jan"));
        mockMvc.perform(post("/loans").param("bookId", "2").param("borrower", "Anna"));
        mockMvc.perform(post("/loans/1/return"));
    }

    @Test
    @DisplayName("4.0: GET /loans?active=true pokazuje tylko aktywne wypożyczenia")
    void shouldFilterOnlyActiveLoans() throws Exception {
        mockMvc.perform(get("/loans").param("active", "true"))
                .andExpect(status().isOk())
                .andExpect(view().name("loans/list"))
                .andExpect(model().attributeExists("loans"))
                .andExpect(model().attribute("loans", hasSize(1)))
                .andExpect(content().string(org.hamcrest.Matchers.containsString("Anna")))
                .andExpect(content().string(org.hamcrest.Matchers.not(org.hamcrest.Matchers.containsString("Jan"))));
    }
}
