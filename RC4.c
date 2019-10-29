#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<time.h>

unsigned char* RC4encrypt(unsigned char* m, unsigned char* k);
int file_size(char* filename);
int main(int argc, char* argv[]) {
	if (argc == 4) {
		int file_length;
		int file_key_length;
		unsigned char* message;
		unsigned char* key;
		unsigned char* result;


		FILE* frp;
		if (frp = fopen(argv[1], "rb")) {
			file_length = file_size(argv[1]);
			message = (unsigned char*)malloc(file_length + 1);
			fread(message, sizeof(unsigned char), file_length, frp);
			message[file_length] = '\x00';
			fclose(frp);
		}
		else {		
			printf("%s不存在", argv[1]);
			exit(0);
		}
		

		FILE* fkp;
		if (fkp = fopen(argv[3], "rb")) {
			file_key_length = file_size(argv[3]);
			if (file_key_length == 0) {
				printf("%s不能为空", argv[3]);
				exit(0);
			}
			else {
				key = (unsigned char*)malloc(file_key_length + 1);
				fread(key, sizeof(unsigned char), file_key_length, fkp);
				key[file_key_length] = '\x00';
				fclose(fkp);
			}		
		}
		else {
			printf("%s不存在", argv[3]);
			exit(0);
		}
		

		FILE* fwp;
		if (fwp = fopen(argv[2], "wb")) {
			result = (unsigned char*)malloc(file_length);
			clock_t start_time = clock();
			result = RC4encrypt(message, key, file_key_length,file_length);
			clock_t end_time = clock();
			printf("加密完成，用时%f ms", (double)(end_time - start_time));
			fwrite(result, sizeof(unsigned char), file_length, fwp);
			fclose(fwp);
		}
		else {
			printf("%s打开失败", argv[3]);
			exit(0);
		}
	}
	else {
		printf("RC4.exe 加密文件路径 输出文件路径 密钥文件");
	}
	
	return 0;
}

unsigned char* RC4encrypt(unsigned char* m, unsigned char* k,int key_length ,int file_length) {
	unsigned char Sbox[256];
	unsigned char Temp[256];
	for (int i = 0; i < 256; i++) {
		Sbox[i] = i;
		Temp[i] = k[i % key_length];
	}

	unsigned char j = 0;
	unsigned temp;
	for (int i = 0; i < 256; i++) {
		j = (j + Sbox[i] + Temp[i]) % 256;
		temp = Sbox[i];
		Sbox[i] = Sbox[j];
		Sbox[j] = temp;
	}

	unsigned char * result;
	result = (unsigned char*)malloc(file_length);
	unsigned char a=0, b=0;
	unsigned char pos;
	int i;
	for ( i = 0; i < file_length; i++) {
		a = (a + 1) % 256;
		b = (b + Sbox[a]) % 256;
		temp = Sbox[a];
		Sbox[a] = Sbox[b];
		Sbox[b] = temp;
		pos = (Sbox[a] + Sbox[b]) % 256;
		result[i] = m[i] ^ Sbox[pos];
	}
	return result;

}
int file_size(char* filename)
{
	FILE* fp = fopen(filename, "rb");
	if (!fp) return -1;
	fseek(fp, 0L, SEEK_END);
	int size = ftell(fp);
	fclose(fp);

	return size;
}