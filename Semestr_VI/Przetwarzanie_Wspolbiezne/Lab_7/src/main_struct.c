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
    MPI_Datatype minecraft_player_type;
    struct minecraftPlayer player_send, player_recv;
    double start_time, end_time, total_time;

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

    const int nfields = 12;
    int blocklengths[12] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 16, 16, 16};
    MPI_Datatype types[12] = {
        MPI_INT, MPI_INT, MPI_INT, MPI_INT, MPI_INT,
        MPI_DOUBLE,
        MPI_C_BOOL, MPI_C_BOOL, MPI_C_BOOL,
        MPI_CHAR, MPI_CHAR, MPI_CHAR
    };
    MPI_Aint offsets[12];
    MPI_Aint base_address;
    struct minecraftPlayer dummy_player;

    MPI_Get_address(&dummy_player, &base_address);
    MPI_Get_address(&dummy_player.heartsCount, &offsets[0]);
    MPI_Get_address(&dummy_player.foodCount, &offsets[1]);
    MPI_Get_address(&dummy_player.dirtStacks, &offsets[2]);
    MPI_Get_address(&dummy_player.expLevel, &offsets[3]);
    MPI_Get_address(&dummy_player.diamondsCount, &offsets[4]);
    MPI_Get_address(&dummy_player.weightOfEquipment, &offsets[5]);
    MPI_Get_address(&dummy_player.weponized, &offsets[6]);
    MPI_Get_address(&dummy_player.armored, &offsets[7]);
    MPI_Get_address(&dummy_player.premiumPlayer, &offsets[8]);
    MPI_Get_address(&dummy_player.gameMode, &offsets[9]);
    MPI_Get_address(&dummy_player.skinName, &offsets[10]);
    MPI_Get_address(&dummy_player.nickname, &offsets[11]);

    for (int i = 0; i < nfields; ++i) {
        offsets[i] = MPI_Aint_diff(offsets[i], base_address);
    }

    MPI_Type_create_struct(nfields, blocklengths, offsets, types, &minecraft_player_type);
    MPI_Type_commit(&minecraft_player_type);

    if (rank == 0) {
        initializePlayer(&player_send);
        printf("Rozpoczynanie transmisji (typ strukturalny) dla %d procesów i %d powtórzeń...\n", size, N_TRANSMISSIONS);
    }

    MPI_Barrier(MPI_COMM_WORLD);

    start_time = MPI_Wtime();

    for (int i = 0; i < N_TRANSMISSIONS; ++i) {
        if (rank == 0) {
            MPI_Send(&player_send, 1, minecraft_player_type, nextrank, 0, MPI_COMM_WORLD);
            MPI_Recv(&player_recv, 1, minecraft_player_type, prevrank, 0, MPI_COMM_WORLD, &status);
             memcpy(&player_send, &player_recv, sizeof(struct minecraftPlayer));
        } else {
            MPI_Recv(&player_recv, 1, minecraft_player_type, prevrank, 0, MPI_COMM_WORLD, &status);
            MPI_Send(&player_recv, 1, minecraft_player_type, nextrank, 0, MPI_COMM_WORLD);
        }
    }

    MPI_Barrier(MPI_COMM_WORLD);
    end_time = MPI_Wtime();

    if (rank == 0) {
        total_time = end_time - start_time;
        printf("Zakończono transmisje.\n");
        printf("Całkowity czas dla %d transmisji (typ strukturalny): %f sekund\n", N_TRANSMISSIONS, total_time);
        printf("Średni czas na transmisję: %f sekund\n", total_time / N_TRANSMISSIONS);

        FILE *outfile = fopen("wyniki_struct.csv", "a");
        if (outfile != NULL) {
            fseek(outfile, 0, SEEK_END);
            long size_of_file = ftell(outfile);
            if (size_of_file == 0) {
                 fprintf(outfile, "LiczbaProcesow,LiczbaTransmisji,CzasCalkowity(s),CzasSredni(s)\n");
            }
            // Zapisz dane
            fprintf(outfile, "%d,%d,%f,%f\n", size, N_TRANSMISSIONS, total_time, total_time / N_TRANSMISSIONS);
            fclose(outfile);
            printf("Wyniki zapisano do pliku\n");
        } else {
            perror("Nie można otworzyć pliku do zapisu");
        }
    }

    MPI_Type_free(&minecraft_player_type);

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
