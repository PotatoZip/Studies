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
import static org.hamcrest.Matchers.startsWith;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@Import(TestClockConfig.class)
class Grade3BooksListPageTest {

    @Autowired
    MockMvc mockMvc;
    @Autowired
    LibraryStore store;

    @BeforeEach
    void setup() {
        store.resetWithSampleData();
    }

    @Test
    @DisplayName("3.0: GET /books renderuje widok listy książek i przekazuje model")
    void shouldRenderBooksListPage() throws Exception {
        mockMvc.perform(get("/books"))
                .andExpect(status().isOk())
                .andExpect(view().name("books/list"))
                .andExpect(model().attributeExists("books"))
                .andExpect(model().attribute("books", hasSize(3)))
                .andExpect(content().string(org.hamcrest.Matchers.containsString("Clean Code")))
                .andExpect(content().string(org.hamcrest.Matchers.containsString("Effective Java")))
                .andExpect(content().string(org.hamcrest.Matchers.containsString("<!doctype html>")));
    }
}
