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
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@Import(TestClockConfig.class)
class Grade4DashboardPageTest {

    @Autowired MockMvc mockMvc;
    @Autowired LibraryStore store;

    @BeforeEach
    void setup() {
        store.resetWithSampleData();
    }

    @Test
    @DisplayName("4.0: GET /dashboard pokazuje poprawne agregaty biblioteki")
    void shouldRenderDashboardWithAggregates() throws Exception {
        mockMvc.perform(post("/loans")
                .param("bookId", "1")
                .param("borrower", "Jan"));

        mockMvc.perform(get("/dashboard"))
                .andExpect(status().isOk())
                .andExpect(view().name("dashboard"))
                .andExpect(model().attributeExists("dashboard"))
                .andExpect(content().string(org.hamcrest.Matchers.containsString("Books: 3")))
                .andExpect(content().string(org.hamcrest.Matchers.containsString("Total copies: 7")))
                .andExpect(content().string(org.hamcrest.Matchers.containsString("Available copies: 6")))
                .andExpect(content().string(org.hamcrest.Matchers.containsString("Active loans: 1")));
    }
}
