// Zadanie 1

import java.util.Random;

public class SumOfVectors {

    private static final int N = 10000;
    private static final int NUM_THREADS = 8;

    private static int[] vectorA = new int[N];
    private static int[] vectorB = new int[N];
    private static int[] resultVector = new int[N];

    public static void main(String[] args) {
        initializeVectors();

        Thread[] threads = new Thread[NUM_THREADS];
        
        int elementsPerThread = N / NUM_THREADS;
        int remainingElements = N % NUM_THREADS;

        int startIndex = 0;
        for (int i = 0; i < NUM_THREADS; i++) {
            int endIndex = startIndex + elementsPerThread - 1;
            if (i == NUM_THREADS - 1) {
                endIndex += remainingElements;
            }
            
            threads[i] = new SummingThread(startIndex, endIndex);
            threads[i].start();
            startIndex = endIndex + 1;
        }

        for (int i = 0; i < NUM_THREADS; i++) {
            try {
                threads[i].join();
            } catch (InterruptedException e) {
                System.err.println("Wątek został przerwany: " + e.getMessage());
            }
        }

        System.out.println("Suma wektorów (pierwsze 20 elementów):");
        for (int i = 0; i < Math.min(20, N); i++) {
            System.out.print(resultVector[i] + " ");
        }
        System.out.print("\n");
        System.out.println("Suma wektorów (ostatnie 20 elementów):");
        for (int i = Math.max(0, N - 20); i < N; i++) {
            System.out.print(resultVector[i] + " ");
        }
        System.out.println();
    }

    static class SummingThread extends Thread {
        private final int startIndex;
        private final int endIndex;

        public SummingThread(int startIndex, int endIndex) {
            this.startIndex = startIndex;
            this.endIndex = endIndex;
        }

        @Override
        public void run() {
            for (int i = startIndex; i <= endIndex; i++) {
                resultVector[i] = vectorA[i] + vectorB[i];
            }
        }
    }

    private static void initializeVectors() {
        Random random = new Random();
        for (int i = 0; i < N; i++) {
            vectorA[i] = random.nextInt(100);
            vectorB[i] = random.nextInt(100);
        }
        System.out.println("Wektory A i B zainicjalizowane o długości N = " + N);
        System.out.println("Wykorzystano wątków: " + NUM_THREADS);
    }
}