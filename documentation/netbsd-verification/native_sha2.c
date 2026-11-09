/* Verify the MuPDF SHA-2 implementation after NetBSD build patches. */
#include <stdio.h>
#include <mupdf/fitz.h>

static void print_digest(const unsigned char *digest, size_t length)
{
    size_t index;
    for (index = 0; index < length; ++index)
        printf("%02x", digest[index]);
    putchar('\n');
}

int main(void)
{
    const unsigned char input[] = "abc";
    unsigned char digest256[32], digest512[64];
    fz_sha256 context256;
    fz_sha512 context512;

    fz_sha256_init(&context256);
    fz_sha256_update(&context256, input, 3);
    fz_sha256_final(&context256, digest256);
    fz_sha512_init(&context512);
    fz_sha512_update(&context512, input, 3);
    fz_sha512_final(&context512, digest512);
    print_digest(digest256, sizeof(digest256));
    print_digest(digest512, sizeof(digest512));
    return 0;
}
