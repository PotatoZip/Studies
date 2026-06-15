package pl.example.lab6.view;

public record DashboardView(
        int booksCount,
        int totalCopies,
        int availableCopies,
        int activeLoans
) {
}
