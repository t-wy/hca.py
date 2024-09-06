﻿
//--------------------------------------------------
// インクルード
//--------------------------------------------------
#define WIN32_LEAN_AND_MEAN
#if _WIN32
	#include <Windows.h>
#else
	#include <cstring>
#endif
#ifndef MAX_PATH
	#define MAX_PATH 260
#endif
#include <stdio.h>
#include "clHCA.h"
#ifndef strcpy_s
	#define strcpy_s(a,b,c) strcpy(a,c)
#endif
#ifndef strcat_s
	#define strcat_s(a,b,c) strcat(a,c)
#endif

//--------------------------------------------------
// 文字列を10進数とみなして数値に変換(簡易版)
//--------------------------------------------------
int _atoi(const char* s) {
	int r = 0;
	bool sign = false; if (*s == '+') { s++; }
	else if (*s == '-') { sign = true; s++; }
	while (*s) {
		if (*s >= '0' && *s <= '9')r = r * 10 + (*s - '0');
		else break;
		s++;
	}
	return sign ? -r : r;
}
float _atof(const char* s) {
	int r1 = 0, r2 = 0, c = 1;
	bool sign = false; if (*s == '+') { s++; }
	else if (*s == '-') { sign = true; s++; }
	while (*s) {
		if (*s >= '0' && *s <= '9')r1 = r1 * 10 + (*s - '0');
		else break;
		s++;
	}
	if (*s == '.') {
		s++;
		while (*s) {
			if (*s >= '0' && *s <= '9') { r2 = r2 * 10 + (*s - '0'); c *= 10; }
			else break;
			s++;
		}
	}
	float r = r1 + ((c > 0) ? r2 / (float)c : 0);
	return sign ? -r : r;
}

//--------------------------------------------------
// 文字列を16進数とみなして数値に変換
//--------------------------------------------------
long long atoi16(const char* s) {
	long long r = 0;
	bool sign = false; if (*s == '+') { s++; }
	else if (*s == '-') { sign = true; s++; }
	while (*s) {
		if (*s >= '0' && *s <= '9')r = (r << 4) | (*s - '0');
		else if (*s >= 'A' && *s <= 'F')r = (r << 4) | (*s - 'A' + 10);
		else if (*s >= 'a' && *s <= 'f')r = (r << 4) | (*s - 'a' + 10);
		else break;
		s++;
	}
	return sign ? -r : r;
}

//--------------------------------------------------
// メイン
//--------------------------------------------------
int main(int argc, char* argv[]) {

	// コマンドライン解析
	unsigned int count = 0;
	char* filenameOut = NULL;
	//bool decodeFlg=false;
	float volume = 1;
	unsigned long long ciphKey = 0xCF222F1FE0748978LL;
	unsigned short subkey = 0;
	int mode = 16;
	int loop = 0;
	bool info = false;
	bool decrypt = false;
	for (int i = 1; i < argc; i++) {
		if (argv[i][0] == '-') {
			switch (argv[i][1]) {
			case 'o':if (i + 1 < argc) { filenameOut = argv[++i]; }break;
				//case 'd':decodeFlg=true;break;
			case 'v':volume = (float)_atof(argv[++i]); break;
			case 'a':if (i + 1 < argc) { ciphKey ^= (ciphKey & 0xffffffffLL) ^ atoi16(argv[++i]); }break;
			case 'b':if (i + 1 < argc) { ciphKey ^= (ciphKey & 0xffffffff00000000LL) ^ (atoi16(argv[++i]) << 32); }break;
			case 'k':if (i + 1 < argc) { ciphKey = atoi16(argv[++i]); }break;
			case 's':if (i + 1 < argc) { subkey = _atoi(argv[++i]); }break;
			case 'm':if (i + 1 < argc) { mode = _atoi(argv[++i]); }break;
			case 'l':if (i + 1 < argc) { loop = _atoi(argv[++i]); }break;
			case 'i':info = true; break;
			case 'c':decrypt = true; break;
			}
		}
		else if (*argv[i]) {
			argv[count++] = argv[i];
		}
	}
	if (subkey) {
		ciphKey = ciphKey * ( ((unsigned long long)subkey << 16u) | ((unsigned short)~subkey + 2u) );
	}

	//if(decodeFlg){

	// 入力チェック
	if (!count) {
		printf("Error: 入力ファイルを指定してください。\n");
		return -1;
	}

	// デコード
	for (unsigned int i = 0; i < count; i++) {

		// 2つ目以降のファイルは、出力ファイル名オプションが無効
		if (i)filenameOut = NULL;

		// デフォルト出力ファイル名
		char path[MAX_PATH];
		if (!(filenameOut && filenameOut[0])) {
			strcpy_s(path, sizeof(path), argv[i]);
			char* d1 = strrchr(path, '\\');
			char* d2 = strrchr(path, '/');
			char* e = strrchr(path, '.');
			if (e && d1 < e && d2 < e)*e = '\0';
			strcat_s(path, sizeof(path), ".wav");
			filenameOut = path;
		}

		// ヘッダ情報のみ表示
		if (info) {
			printf("%s のヘッダ情報\n", argv[i]);
			clHCA hca(0);
			hca.PrintInfo(argv[i]);
			printf("\n");
		}

		// 復号化
		else if (decrypt) {
			printf("%s を復号化中...\n", argv[i]);
			clHCA hca(ciphKey);
			if (!hca.Decrypt(argv[i])) {
				printf("Error: 復号化に失敗しました。\n");
			}
		}

		// デコード
		else {
			printf("%s をデコード中...\n", argv[i]);
			clHCA hca(ciphKey);
			if (!hca.DecodeToWavefile(argv[i], filenameOut, volume, mode, loop)) {
				printf("Error: デコードに失敗しました。\n");
			}
		}

	}

	//}

	return 0;
}
