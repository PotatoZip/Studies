#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <libssh2.h>
#include <libssh2_sftp.h>
#include "libcommon.h"

#define PASS_LEN 128
#define BUF_SIZE 1024
#define PATH_BUF_SIZE 2048

int authenticate_user(LIBSSH2_SESSION *session, struct connection_data *cd,
                      const char* pubkey, const char* privkey,
                      const char* passphrase);

int main(int argc, char **argv) {

    int                 err;
    int                 sockfd; /* Socket descriptor */
    char                dir[PATH_BUF_SIZE]; /* Buffer for directory path */
    char                filename[BUF_SIZE]; /* Filename buffer for listing */
    char                remote_filepath[PATH_BUF_SIZE]; /* Full remote file path */
    char                local_filepath[BUF_SIZE]; /* Local filename to save */
    char                mem[BUF_SIZE]; /* Buffer for I/O operations */
    int                 bytes; /* Number of bytes read/written */
    long                total_bytes_downloaded = 0; // Track download size

    struct connection_data  *cd; /* Program arguments */
    LIBSSH2_SESSION         *session; /* SSH session object */
    LIBSSH2_SFTP            *sftp; /* SFTP subsystem session */
    LIBSSH2_SFTP_HANDLE     *dir_handle; /* SFTP directory handle */
    LIBSSH2_SFTP_HANDLE     *file_handle; /* SFTP file handle */
    FILE                    *local_fp = NULL; /* Local file pointer */

    cd = parse_connection_data(argc, argv, CD_ADDRESS | CD_USERNAME);
    if (cd == NULL) {
        exit(EXIT_FAILURE);
    }

    /* Initialize libssh2 */
    err = libssh2_init(0);
    if (err != 0) {
        fprintf(stderr, "libssh2 initialization failed (%d)\n", err);
        exit(EXIT_FAILURE);
    }


    /*
     * Establish TCP connection. Returns descriptor for the connected socket.
     * Connection data is passed via connection_data structure pointer.
     */
    sockfd = establish_tcp_connection(cd);
    if (sockfd == -1) {
        libssh2_exit();
        exit(EXIT_FAILURE);
    }

    /*
     * Initialize the structure representing the Transport Layer Protocol session.
     */
    session = libssh2_session_init();
    if (session == NULL) {
        fprintf(stderr, "libssh2_session_init() failed!\n");
        close(sockfd);
        libssh2_exit();
        exit(EXIT_FAILURE);
    }

    /*
     * Start SSH connection parameter negotiation, secret key exchange,
     * and SSH server authentication.
     */
    err = libssh2_session_handshake(session, sockfd); // Use handshake instead of startup
    if (err < 0) {
        print_ssh_error(session, "libssh2_session_handshake()");
        libssh2_session_free(session);
        close(sockfd);
        libssh2_exit();
        exit(EXIT_FAILURE);
    }

    err = authenticate_server(session);
    if (err < 0) {
        libssh2_session_disconnect(session, "Server authentication failed");
        libssh2_session_free(session);
        close(sockfd);
        libssh2_exit();
        exit(EXIT_FAILURE);
    }

    err = authenticate_user(session, cd, "public.key", "private.key", "passphrase");
    if (err < 0) {
        fprintf(stderr, "User authentication failed.\n");
        libssh2_session_disconnect(session, "Authentication failed");
        libssh2_session_free(session);
        close(sockfd);
        libssh2_exit();
        exit(EXIT_FAILURE);
    }

    fprintf(stdout, "User authentication successful.\n");

    /* Initialize the "sftp" subsystem. */
    sftp = libssh2_sftp_init(session);
    if (sftp == NULL) {
        fprintf(stderr, "libssh2_sftp_init() failed!\n");
        if (libssh2_session_last_errno(session) == LIBSSH2_ERROR_EAGAIN) {
            fprintf(stderr, "Non-blocking mode error, try again later.\n");
        } else if (libssh2_session_last_errno(session) == LIBSSH2_ERROR_ALLOC) {
            fprintf(stderr, "Memory allocation error.\n");
        } else if (libssh2_session_last_errno(session) == LIBSSH2_ERROR_SOCKET_SEND || libssh2_session_last_errno(session) == LIBSSH2_ERROR_SOCKET_TIMEOUT) {
             fprintf(stderr, "Socket send/timeout error.\n");
        } else if (libssh2_session_last_errno(session) == LIBSSH2_ERROR_SFTP_PROTOCOL) {
             fprintf(stderr, "SFTP protocol error (maybe subsystem not enabled on server?).\n");
        } else {
             print_ssh_error(session, "libssh2_sftp_init()");
        }
        libssh2_session_disconnect(session, "SFTP init failed");
        libssh2_session_free(session);
        close(sockfd);
        libssh2_exit();
        exit(EXIT_FAILURE);
    }

     fprintf(stdout, "SFTP session initialized.\n");

    snprintf(dir, PATH_BUF_SIZE, "/home/%s", cd->username);
    fprintf(stdout, "Listing contents of remote directory: %s\n", dir);


    /* Get SFTP handle to the remote directory. */
    dir_handle = libssh2_sftp_opendir(sftp, dir);
    if (dir_handle == NULL) {
        print_sftp_error(session, sftp, "libssh2_sftp_opendir()");
        if(libssh2_sftp_last_error(sftp) == LIBSSH2_FX_NO_SUCH_FILE) {
            fprintf(stderr, "Error: Directory '%s' not found on server.\n", dir);
        } else if (libssh2_sftp_last_error(sftp) == LIBSSH2_FX_PERMISSION_DENIED) {
            fprintf(stderr, "Error: Permission denied to open directory '%s'.\n", dir);
        }
        libssh2_sftp_shutdown(sftp);
        libssh2_session_disconnect(session, "Failed to open remote directory");
        libssh2_session_free(session);
        close(sockfd);
        libssh2_exit();
        exit(EXIT_FAILURE);
    }

    /* List directory contents: */
    fprintf(stdout, "-------------------------------------------\n");
    do {
        LIBSSH2_SFTP_ATTRIBUTES attrs; // To potentially get file type info if needed

        // Use readdir_ex to get attributes as well, though 'mem' often contains ls -l like output
        bytes = libssh2_sftp_readdir_ex(dir_handle, filename, BUF_SIZE,
                                        mem, BUF_SIZE, &attrs);

        if (bytes > 0) {

            if (strlen(mem) > 0) {
                /* If detailed listing is available. */
                fprintf(stdout, "%s\n", mem);
            } else {
                 /* Fallback to just the filename */
                fprintf(stdout, "%s\n", filename);
            }
             // Clear buffers for next iteration
             memset(filename, 0, BUF_SIZE);
             memset(mem, 0, BUF_SIZE);
        } else if (bytes < 0) {
            // Error occurred during listing
            print_sftp_error(session, sftp, "libssh2_sftp_readdir_ex()");
            libssh2_sftp_closedir(dir_handle); // Attempt cleanup
            libssh2_sftp_shutdown(sftp);
            libssh2_session_disconnect(session, "Failed to read directory");
            libssh2_session_free(session);
            close(sockfd);
            libssh2_exit();
            exit(EXIT_FAILURE);
        }
        // bytes == 0 means end of directory listing

    } while (bytes > 0);
    fprintf(stdout, "-------------------------------------------\n");

    /* Close SFTP directory handle. */
    err = libssh2_sftp_closedir(dir_handle);
    if (err < 0) {
        print_sftp_error(session, sftp, "libssh2_sftp_closedir()");
        // Continue shutdown, but log the error
    }

    printf("Enter the filename to download (or press Enter to skip): ");
    fflush(stdout); // Ensure prompt is displayed before input

    // Read filename from user
    if (fgets(local_filepath, BUF_SIZE, stdin) == NULL) {
        fprintf(stderr, "Error reading filename from input.\n");
        // Proceed to shutdown without download attempt
    } else {
        local_filepath[strcspn(local_filepath, "\n")] = 0;

        if (strlen(local_filepath) > 0) {
            fprintf(stdout, "Attempting to download '%s'...\n", local_filepath);

            int dir_len = strlen(dir);
            if (dir_len > 0 && dir[dir_len - 1] != '/') {
                strncat(dir, "/", PATH_BUF_SIZE - dir_len - 1);
            }
            snprintf(remote_filepath, PATH_BUF_SIZE, "%s%s", dir, local_filepath);
            file_handle = libssh2_sftp_open_ex(sftp, remote_filepath,
                                               strlen(remote_filepath),
                                               LIBSSH2_FXF_READ, // Open for reading
                                               0, // Mode (usually ignored for opening existing)
                                               LIBSSH2_SFTP_OPENFILE); // Open a regular file

            if (file_handle == NULL) {
                print_sftp_error(session, sftp, "libssh2_sftp_open_ex()");
                if(libssh2_sftp_last_error(sftp) == LIBSSH2_FX_NO_SUCH_FILE) {
                   fprintf(stderr, "Error: File '%s' not found on server.\n", remote_filepath);
                } else if (libssh2_sftp_last_error(sftp) == LIBSSH2_FX_PERMISSION_DENIED) {
                    fprintf(stderr, "Error: Permission denied to open file '%s'.\n", remote_filepath);
                } else if (libssh2_sftp_last_error(sftp) == LIBSSH2_FX_OP_UNSUPPORTED) {
                     fprintf(stderr, "Error: Server may not support opening this type of item (e.g., a directory).\n");
                }
                // Continue to shutdown
            } else {
                // Open the local file for writing in binary mode
                local_fp = fopen(local_filepath, "wb"); // "wb" for binary write
                if (local_fp == NULL) {
                    perror("Failed to open local file for writing");
                    libssh2_sftp_close(file_handle); // Close remote handle
                    // Continue to shutdown
                } else {
                    fprintf(stdout, "Downloading %s to local file %s\n", remote_filepath, local_filepath);
                    total_bytes_downloaded = 0;
                    // Read loop
                    do {
                        bytes = libssh2_sftp_read(file_handle, mem, BUF_SIZE);
                        if (bytes > 0) {
                            // Write the read data to the local file
                            size_t written = fwrite(mem, 1, bytes, local_fp);
                            if (written != (size_t)bytes) {
                                perror("Error writing to local file");
                                bytes = -1; // Signal error to break loop
                            } else {
                                total_bytes_downloaded += bytes;
                            }
                        } else if (bytes < 0) {
                            // Error reading from remote file
                            print_sftp_error(session, sftp, "libssh2_sftp_read()");
                        }
                        // bytes == 0 means EOF
                    } while (bytes > 0);

                    // Close the local file
                    if (fclose(local_fp) != 0) {
                        perror("Error closing local file");
                    } else {
                         if (bytes == 0) { // Check if loop finished due to EOF (success)
                            fprintf(stdout, "Download complete. Total bytes: %ld\n", total_bytes_downloaded);
                         } else {
                             fprintf(stderr, "Download failed or was interrupted.\n");
                             // Optionally remove the potentially incomplete local file
                             // remove(local_filepath);
                         }
                    }

                    // Close the remote file handle
                    err = libssh2_sftp_close(file_handle);
                    if (err < 0) {
                        print_sftp_error(session, sftp, "libssh2_sftp_close()");
                    }
                } // End local file open check
            } // End remote file open check
        } else {
             fprintf(stdout, "Skipping download.\n");
        }
    } // End fgets check


    err = libssh2_sftp_shutdown(sftp);
    if (err < 0) {
        print_sftp_error(session, sftp, "libssh2_sftp_shutdown()");
        // Log error, but continue shutdown
    }
     fprintf(stdout, "SFTP session shut down.\n");

    /* Close the Transport Layer Protocol session (SSH connection). */
    err = libssh2_session_disconnect(session, "Graceful shutdown");
    if (err < 0) {
        print_ssh_error(session, "libssh2_session_disconnect()");
        // Log error, but continue cleanup
    }

    /* Free resources associated with the SSH session. */
    libssh2_session_free(session);

    /* Close the TCP socket. */
    close(sockfd);
     fprintf(stdout, "TCP connection closed.\n");

    /* Free memory allocated for command-line arguments. */
    free_connection_data(cd);

    /* Clean up libssh2 */
    libssh2_exit();

    exit(EXIT_SUCCESS);
}


/*
 * Tries authentication using public key, and if it's not
 * supported by the server or fails, it uses the "password" method.
 * Assumes get_password is defined in libcommon.c
 */
int authenticate_user(LIBSSH2_SESSION *session, struct connection_data *cd,
                      const char* pubkey, const char* privkey,
                      const char* passphrase) {

    int   err = -1; // Default to error
    char *auth_list = NULL;
    char  password[PASS_LEN];
    int   auth_methods_tried = 0;

    /* Get the list of methods supported by the SSH server. */
    /* Note: This can return NULL if "none" auth succeeded, or on error */
    auth_list = libssh2_userauth_list(session, cd->username, strlen(cd->username));

    if (auth_list == NULL) {
        if (libssh2_userauth_authenticated(session)) {
            // This happens if the server allows "none" authentication method
            fprintf(stderr, "Warning: USERAUTH_NONE succeeded! No password or key needed.\n");
            return 0; // Successfully authenticated (though potentially insecure setup)
        } else {
            // Error occurred trying to get the list
            print_ssh_error(session, "libssh2_userauth_list()");
            return -1; // Indicate failure
        }
    }

    fprintf(stdout, "Supported authentication methods: %s\n", auth_list);

    /* Check if the server supports the "publickey" method. */
    if (strstr(auth_list, "publickey") != NULL) {
        auth_methods_tried++;
        fprintf(stdout, "Attempting public key authentication...\n");
        /*
         * Authenticate using public key.
         * cd->username - username
         * pubkey - path to public key
         * privkey - path to private key
         * passphrase - password protecting access to the private key (can be NULL or "")
         */
        err = libssh2_userauth_publickey_fromfile(session, cd->username,
                pubkey, privkey, passphrase);

        if (err == 0) {
            fprintf(stdout, "Public key authentication successful!\n");
            return 0; // Success
        } else {
             // Key auth failed, print why
             if (err == LIBSSH2_ERROR_EAGAIN) {
                 fprintf(stderr, "Public key auth error: Non-blocking I/O, try again.\n");
             } else if (err == LIBSSH2_ERROR_ALLOC) {
                 fprintf(stderr, "Public key auth error: Memory allocation failed.\n");
             } else if (err == LIBSSH2_ERROR_SOCKET_SEND || err == LIBSSH2_ERROR_SOCKET_TIMEOUT) {
                 fprintf(stderr, "Public key auth error: Socket send/timeout.\n");
             } else if (err == LIBSSH2_ERROR_PUBLICKEY_UNVERIFIED) {
                 fprintf(stderr, "Public key auth error: Public key is invalid or not accepted by server.\n");
             } else if (err == LIBSSH2_ERROR_AUTHENTICATION_FAILED) {
                  fprintf(stderr, "Public key auth error: Authentication failed (bad key, wrong user, wrong passphrase?).\n");
             } else if (err == LIBSSH2_ERROR_FILE) {
                   fprintf(stderr, "Public key auth error: Problem reading key files ('%s', '%s'). Check paths and permissions.\n", pubkey, privkey);
             } else {
                 print_ssh_error(session, "libssh2_userauth_publickey_fromfile()");
             }
             // Don't return yet, try password auth if available
        }
    }

    /* Check if the server supports the "password" method. */
    if (strstr(auth_list, "password") != NULL) {
        auth_methods_tried++;
        fprintf(stdout, "Attempting password authentication...\n");
        for (int attempts = 0; attempts < 3; ++attempts) { // Limit password attempts

            /* Get user password. Assumes get_password is in libcommon.c */
            if (get_password("Password: ", password, PASS_LEN)) {
                fprintf(stderr, "get_password() failed!\n");
                memset(password, 0, PASS_LEN); // Clear potentially sensitive data
                return -1; // Indicate failure
            }

            /* Authenticate using password. */
            err = libssh2_userauth_password(session, cd->username, password);
            memset(password, 0, PASS_LEN); // Clear password from memory ASAP

            if (err == 0) {
                fprintf(stdout, "Password authentication successful!\n");
                return 0; // Success
            } else {
                 if (err == LIBSSH2_ERROR_EAGAIN) {
                     fprintf(stderr, "Password auth error: Non-blocking I/O, try again.\n");
                     // May need to handle this differently in non-blocking app
                 } else if (err == LIBSSH2_ERROR_ALLOC) {
                     fprintf(stderr, "Password auth error: Memory allocation failed.\n");
                 } else if (err == LIBSSH2_ERROR_SOCKET_SEND || err == LIBSSH2_ERROR_SOCKET_TIMEOUT) {
                     fprintf(stderr, "Password auth error: Socket send/timeout.\n");
                 } else if (err == LIBSSH2_ERROR_AUTHENTICATION_FAILED) {
                     fprintf(stderr, "Authentication failed! (Attempt %d/3)\n", attempts + 1);
                     // Loop continues for more attempts
                 } else {
                     print_ssh_error(session, "libssh2_userauth_password()");
                     return -1; // Unhandled error
                 }
            }
        }
        // If loop finishes, all password attempts failed
        fprintf(stderr, "Password authentication failed after multiple attempts.\n");
        return -1; // Failure
    }

    // If we reach here, either no supported methods were found,
    // or the attempted methods failed.
    if (auth_methods_tried == 0) {
        fprintf(stderr, "No supported authentication methods (publickey, password) found on server.\n");
    } else {
         fprintf(stderr, "All attempted authentication methods failed.\n");
    }

    return -1; // Indicate failure
}