// Zadanie 2

import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.concurrent.ConcurrentHashMap;

public class ImageHistogram {

    private static final int N_ROWS = 1000;
    private static final int M_COLS = 1000;
    private static final int NUM_THREADS = 4;

    private static char[][] image = new char[N_ROWS][M_COLS];

    private static ConcurrentHashMap<Character, Integer> globalHistogram = new ConcurrentHashMap<>();

    private static final char[] POSSIBLE_CHARS = {
        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
        '-', '_', '+', '=', '[', ']', '{', '}', ';', ':',
        '\'', '"', ',', '.', '/', '<', '>', '?', '~', '`'
    };

    public static void main(String[] args) {
        initializeImage();
        System.out.println("Obraz o wymiarach " + N_ROWS + "x" + M_COLS + " zainicjalizowany.");

        Map<Integer, char[]> threadCharAssignments = assignCharsToThreads(POSSIBLE_CHARS, NUM_THREADS);

        Thread[] threads = new Thread[NUM_THREADS];
        for (int i = 0; i < NUM_THREADS; i++) {
            char[] assignedChars = threadCharAssignments.get(i);
            if (assignedChars != null) {
                threads[i] = new HistogramThread(i, assignedChars);
                threads[i].start();
            }
        }

        for (int i = 0; i < NUM_THREADS; i++) {
            if (threads[i] != null) {
                try {
                    threads[i].join();
                } catch (InterruptedException e) {
                    System.err.println("Wątek " + i + " został przerwany: " + e.getMessage());
                }
            }
        }

        System.out.println("\n--- Końcowy Histogram ---");
        globalHistogram.entrySet()
                .stream()
                .sorted(Map.Entry.comparingByKey())
                .forEach(entry -> System.out.println("Znak '" + entry.getKey() + "': " + entry.getValue() + " wystąpień"));
    }

    static class HistogramThread extends Thread {
        private final int threadId;
        private final char[] charsToCount;

        public HistogramThread(int threadId, char[] charsToCount) {
            this.threadId = threadId;
            this.charsToCount = charsToCount;
            System.out.println("Wątek " + threadId + " odpowiedzialny za znaki: " + new String(charsToCount));
        }

        @Override
        public void run() {
            Map<Character, Integer> localHistogram = new HashMap<>();
            for (char c : charsToCount) {
                localHistogram.put(c, 0);
            }

            for (int r = 0; r < N_ROWS; r++) {
                for (int c = 0; c < M_COLS; c++) {
                    char currentChar = image[r][c];
                    if (localHistogram.containsKey(currentChar)) {
                        localHistogram.put(currentChar, localHistogram.get(currentChar) + 1);
                    }
                }
            }

            for (Map.Entry<Character, Integer> entry : localHistogram.entrySet()) {
                globalHistogram.merge(entry.getKey(), entry.getValue(), Integer::sum);
            }
            System.out.println("Wątek " + threadId + " zakończył przetwarzanie.");
        }
    }

    private static void initializeImage() {
        Random random = new Random();
        for (int r = 0; r < N_ROWS; r++) {
            for (int c = 0; c < M_COLS; c++) {
                image[r][c] = POSSIBLE_CHARS[random.nextInt(POSSIBLE_CHARS.length)];
            }
        }
    }

    private static Map<Integer, char[]> assignCharsToThreads(char[] allChars, int numThreads) {
        Map<Integer, char[]> assignments = new HashMap<>();
        int charsPerThread = allChars.length / numThreads;
        int remainingChars = allChars.length % numThreads;

        int charIndex = 0;
        for (int i = 0; i < numThreads; i++) {
            int currentThreadCharsCount = charsPerThread;
            if (i < remainingChars) {
                currentThreadCharsCount++;
            }

            char[] assigned = new char[currentThreadCharsCount];
            System.arraycopy(allChars, charIndex, assigned, 0, currentThreadCharsCount);
            assignments.put(i, assigned);
            charIndex += currentThreadCharsCount;
        }
        return assignments;
    }
}