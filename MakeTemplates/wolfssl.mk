# /usr/bin/make -f wolfssl.mk


WOLFSSL_ROOT = ./wolfssl
LIBWOLFSSL = $(WOLFSSL_ROOT)/libwolfssl.a


OPT_FLAGS = -Os -g
INC_PATHS = -I$(WOLFSSL_ROOT)
#INC_OPTIONS = -include $(WOLFSSL_ROOT)/wolfssl/options.h
USER_SETTINGS = -DWOLFSSL_USER_SETTINGS -I.

OPT_APPLE = -framework CoreFoundation -framework Security

CFLAGS = $(OPT_FLAGS) $(INC_PATHS) $(USER_SETTINGS) $(INC_OPTIONS)

SRC = $(WOLFSSL_ROOT)/src/crl.c \
	$(WOLFSSL_ROOT)/src/dtls.c \
	$(WOLFSSL_ROOT)/src/dtls13.c \
	$(WOLFSSL_ROOT)/src/internal.c \
	$(WOLFSSL_ROOT)/src/keys.c \
	$(WOLFSSL_ROOT)/src/ocsp.c \
	$(WOLFSSL_ROOT)/src/quic.c \
	$(WOLFSSL_ROOT)/src/sniffer.c \
	$(WOLFSSL_ROOT)/src/ssl.c \
	$(WOLFSSL_ROOT)/src/tls.c \
	$(WOLFSSL_ROOT)/src/tls13.c \
	$(WOLFSSL_ROOT)/src/wolfio.c

SRC_CRYPT = $(WOLFSSL_ROOT)/wolfcrypt/src/aes.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/arc4.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/asm.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/asn.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/async.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/blake2b.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/blake2s.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/camellia.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/chacha.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/chacha20_poly1305.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/cmac.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/coding.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/compress.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/cpuid.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/cryptocb.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/curve25519.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/curve448.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/des3.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/dh.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/dilithium.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/dsa.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/ecc.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/ecc_fp.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/eccsi.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/ed25519.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/ed448.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/error.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/ext_kyber.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/falcon.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/fe_448.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/fe_low_mem.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/fe_operations.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/fips.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/fips_test.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/ge_448.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/ge_low_mem.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/ge_operations.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/hash.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/hmac.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/hpke.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/integer.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/kdf.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/logging.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/md2.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/md4.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/md5.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/memory.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/pkcs12.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/pkcs7.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/poly1305.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/pwdbased.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/random.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/rc2.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/ripemd.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/rsa.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sakke.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/selftest.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sha.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sha256.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sha3.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sha512.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/signature.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/siphash.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sp_arm32.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sp_arm64.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sp_armthumb.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sp_c32.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sp_c64.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sp_cortexm.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sp_dsp32.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sp_int.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sp_x86_64.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/sphincs.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/srp.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/tfm.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/wc_dsp.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/wc_encrypt.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/wc_kyber.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/wc_kyber_poly.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/wc_pkcs11.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/wc_port.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/wolfcrypt_first.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/wolfcrypt_last.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/wolfevent.c \
	$(WOLFSSL_ROOT)/wolfcrypt/src/wolfmath.c

OBJECT = $(SRC:.c=.o) $(SRC_CRYPT:.c=.o)

PROGRAM = $(WOLFSSL_ROOT)/examples/server/server \
	$(WOLFSSL_ROOT)/examples/echoserver/echoserver



all: library program

library: $(LIBWOLFSSL)
$(LIBWOLFSSL): $(OBJECT)
	ar r $@ $(OBJECT)

$(OBJECT): %.o : %.c
	gcc -o $@ -c $^ $(CFLAGS)

program: $(PROGRAM)
$(PROGRAM): % : %.c
	gcc -o $@ $^ $(LIBWOLFSSL) $(CFLAGS)  $(OPT_APPLE)

clean:
	rm -f $(OBJECT)
	rm -f $(LIBWOLFSSL)
	rm -f $(PROGRAM)
