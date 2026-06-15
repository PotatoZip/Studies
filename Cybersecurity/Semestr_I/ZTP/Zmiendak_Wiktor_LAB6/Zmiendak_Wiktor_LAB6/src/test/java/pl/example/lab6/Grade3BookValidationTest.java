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
class Grade3BookValidationTest {

    @Autowired MockMvc mockMvc;
    @Autowired LibraryStore store;

    @BeforeEach
    void setup() {
        store.resetWithSampleData();
    }

    @Test
    @DisplayName("3.0: Formularz książki używa Bean Validation i przy błędzie wraca do widoku form")
    void shouldValidateBookForm() throws Exception {
        mockMvc.perform(post("/books")
                        .param("title", "")
                        .param("author", "")
                        .param("totalCopies", "0"))
                .andExpect(status().isOk())
                .andExpect(view().name("books/form"))
                .andExpect(model().attributeHasFieldErrors("bookForm", "title", "author", "totalCopies"));

        assertEquals(3, store.getBooks().size(), "Validation error should not create a book");
    }
}
