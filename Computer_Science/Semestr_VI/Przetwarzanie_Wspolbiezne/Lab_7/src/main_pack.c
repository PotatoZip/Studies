#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "mpi.h"

#define N_TRANSMISSIONS 1000

struct minecraftPlayer {
    int heartsCount;
    int foodCount;
    int dirtStacks;
    int expLevel;
    int diamondsCount;
    double weightOfEquipment;
    bool weponized;
    bool armored;
    bool premiumPlayer;
    char gameMode[16];
    char skinName[16];
    char nickname[16];
};

void initializePlayer(struct minecraftPlayer *player);
void printPlayer(const struct minecraftPlayer *player, int rank);

int main(int argc, char **argv) {
    int rank, size, nextrank, prevrank;
    struct minecraftPlayer player_send, player_recv;
    double start_time, end_time, total_time;
    char *pack_buffer = NULL;
    int position;
    int buffer_size = 0;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Status status;

    if (size < 2) {
        if (rank == 0) {
            fprintf(stderr, "Ten program wymaga co najmniej 2 procesów MPI.\n");
        }
        MPI_Finalize();
        return 1;
    }

    nextrank = (rank + 1) % size;
    prevrank = (rank - 1 + size) % size;

    int size_int, size_double, size_bool, size_char;
    MPI_Pack_size(1, MPI_INT, MPI_COMM_WORLD, &size_int);
    MPI_Pack_size(1, MPI_DOUBLE, MPI_COMM_WORLD, &size_double);
    MPI_Pack_size(1, MPI_C_BOOL, MPI_COMM_WORLD, &size_bool);
    MPI_Pack_size(1, MPI_CHAR, MPI_COMM_WORLD, &size_char);

    buffer_size = 5 * size_int + 1 * size_double + 3 * size_bool + 16 * size_char + 16 * size_char + 16 * size_char;

    pack_buffer = (char *)malloc(buffer_size);
    if (pack_buffer == NULL) {
        fprintf(stderr, "Rank %d: Nie można zaalokować bufora pakowania o rozmiarze %d!\n", rank, buffer_size);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    if (rank == 0) {
        initializePlayer(&player_send);
        printf("Rozpoczynanie transmisji (typ spakowany) dla %d procesów i %d powtórzeń...\n", size, N_TRANSMISSIONS);
    }

    MPI_Barrier(MPI_COMM_WORLD);

    start_time = MPI_Wtime();

    for (int i = 0; i < N_TRANSMISSIONS; ++i) {
        if (rank == 0) {
            position = 0;
            MPI_Pack(&player_send.heartsCount, 1, MPI_INT, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_send.foodCount, 1, MPI_INT, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_send.dirtStacks, 1, MPI_INT, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_send.expLevel, 1, MPI_INT, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_send.diamondsCount, 1, MPI_INT, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_send.weightOfEquipment, 1, MPI_DOUBLE, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_send.weponized, 1, MPI_C_BOOL, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_send.armored, 1, MPI_C_BOOL, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_send.premiumPlayer, 1, MPI_C_BOOL, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(player_send.gameMode, 16, MPI_CHAR, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(player_send.skinName, 16, MPI_CHAR, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(player_send.nickname, 16, MPI_CHAR, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);

            MPI_Send(pack_buffer, position, MPI_PACKED, nextrank, 0, MPI_COMM_WORLD);

            MPI_Recv(pack_buffer, buffer_size, MPI_PACKED, prevrank, 0, MPI_COMM_WORLD, &status);

            position = 0;
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.heartsCount, 1, MPI_INT, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.foodCount, 1, MPI_INT, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.dirtStacks, 1, MPI_INT, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.expLevel, 1, MPI_INT, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.diamondsCount, 1, MPI_INT, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.weightOfEquipment, 1, MPI_DOUBLE, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.weponized, 1, MPI_C_BOOL, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.armored, 1, MPI_C_BOOL, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.premiumPlayer, 1, MPI_C_BOOL, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, player_recv.gameMode, 16, MPI_CHAR, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, player_recv.skinName, 16, MPI_CHAR, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, player_recv.nickname, 16, MPI_CHAR, MPI_COMM_WORLD);

             memcpy(&player_send, &player_recv, sizeof(struct minecraftPlayer));

        } else {
            MPI_Recv(pack_buffer, buffer_size, MPI_PACKED, prevrank, 0, MPI_COMM_WORLD, &status);

            position = 0;
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.heartsCount, 1, MPI_INT, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.foodCount, 1, MPI_INT, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.dirtStacks, 1, MPI_INT, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.expLevel, 1, MPI_INT, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.diamondsCount, 1, MPI_INT, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.weightOfEquipment, 1, MPI_DOUBLE, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.weponized, 1, MPI_C_BOOL, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.armored, 1, MPI_C_BOOL, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, &player_recv.premiumPlayer, 1, MPI_C_BOOL, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, player_recv.gameMode, 16, MPI_CHAR, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, player_recv.skinName, 16, MPI_CHAR, MPI_COMM_WORLD);
            MPI_Unpack(pack_buffer, buffer_size, &position, player_recv.nickname, 16, MPI_CHAR, MPI_COMM_WORLD);

            position = 0;
            MPI_Pack(&player_recv.heartsCount, 1, MPI_INT, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_recv.foodCount, 1, MPI_INT, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_recv.dirtStacks, 1, MPI_INT, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_recv.expLevel, 1, MPI_INT, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_recv.diamondsCount, 1, MPI_INT, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_recv.weightOfEquipment, 1, MPI_DOUBLE, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_recv.weponized, 1, MPI_C_BOOL, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_recv.armored, 1, MPI_C_BOOL, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(&player_recv.premiumPlayer, 1, MPI_C_BOOL, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(player_recv.gameMode, 16, MPI_CHAR, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(player_recv.skinName, 16, MPI_CHAR, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);
            MPI_Pack(player_recv.nickname, 16, MPI_CHAR, pack_buffer, buffer_size, &position, MPI_COMM_WORLD);

            MPI_Send(pack_buffer, position, MPI_PACKED, nextrank, 0, MPI_COMM_WORLD);
        }
    }

    MPI_Barrier(MPI_COMM_WORLD);
    end_time = MPI_Wtime();

    if (rank == 0) {
        total_time = end_time - start_time;
        printf("Zakończono transmisje.\n");
        printf("Całkowity czas dla %d transmisji (typ spakowany): %f sekund\n", N_TRANSMISSIONS, total_time);
        printf("Średni czas na transmisję: %f sekund\n", total_time / N_TRANSMISSIONS);

        FILE *outfile = fopen("wyniki_packed.csv", "a");
        if (outfile != NULL) {
            fseek(outfile, 0, SEEK_END);
            long size_of_file = ftell(outfile);
            if (size_of_file == 0) {
                fprintf(outfile, "LiczbaProcesow,LiczbaTransmisji,CzasCalkowity(s),CzasSredni(s)\n");
            }
            fprintf(outfile, "%d,%d,%f,%f\n", size, N_TRANSMISSIONS, total_time, total_time / N_TRANSMISSIONS);
            fclose(outfile);
            printf("Wyniki zapisano do pliku\n");
        } else {
            perror("Nie można otworzyć pliku do zapisu");
        }
    }

    free(pack_buffer);

    MPI_Finalize();
    return 0;
}

void initializePlayer(struct minecraftPlayer *player) {
    player->heartsCount = 20;
    player->foodCount = 18;
    player->dirtStacks = 5;
    player->expLevel = 30;
    player->diamondsCount = 64;
    player->weightOfEquipment = 55.8;
    player->weponized = true;
    player->armored = true;
    player->premiumPlayer = false;
    strncpy(player->gameMode, "Survival", 15);
    player->gameMode[15] = '\0';
    strncpy(player->skinName, "Steve", 15);
    player->skinName[15] = '\0';
    strncpy(player->nickname, "Player123", 15);
    player->nickname[15] = '\0';
}

void printPlayer(const struct minecraftPlayer *player, int rank) {
    printf("--- Dane gracza (Rank %d) ---\n", rank);
    printf("  Nickname: %s\n", player->nickname);
    printf("  Hearts: %d\n", player->heartsCount);
    printf("  Food: %d\n", player->foodCount);
    printf("  Dirt Stacks: %d\n", player->dirtStacks);
    printf("  XP Level: %d\n", player->expLevel);
    printf("  Diamonds: %d\n", player->diamondsCount);
    printf("  Equipment Weight: %.2f\n", player->weightOfEquipment);
    printf("  Weaponized: %s\n", player->weponized ? "Yes" : "No");
    printf("  Armored: %s\n", player->armored ? "Yes" : "No");
    printf("  Premium: %s\n", player->premiumPlayer ? "Yes" : "No");
    printf("  Game Mode: %s\n", player->gameMode);
    printf("  Skin Name: %s\n", player->skinName);
    printf("-----------------------------\n");
}