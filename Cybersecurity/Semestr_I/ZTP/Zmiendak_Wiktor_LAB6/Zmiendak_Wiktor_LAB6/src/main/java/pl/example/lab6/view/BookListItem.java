package pl.example.lab6.view;

public record BookListItem(
        Long id,
        String title,
        String author,
        int totalCopies,
        int availableCopies,
        boolean available
) {
}
