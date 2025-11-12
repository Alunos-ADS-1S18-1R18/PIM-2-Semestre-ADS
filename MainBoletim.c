#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <locale.h>


#define RESET   "\x1b[0m"
#define RED     "\x1b[31m"
#define GREEN   "\x1b[32m"
#define YELLOW  "\x1b[33m"
#define CYAN    "\x1b[36m"
#define BOLD    "\x1b[1m"
#define MAX_ALUNOS 200
#define MAX_MATERIAS 50

typedef struct {
    char nome[100];
    char turma[20];
    char ra[40];
    float notas[4];
} Aluno;

typedef struct {
    char nome[100];
    char professor[100];
    Aluno alunos[MAX_ALUNOS];
    int totalAlunos;
} Materia;

Materia materias[MAX_MATERIAS];
int totalMaterias = 0;

/* trim right/left (remove espaços, \r, \n e vírgulas no fim) */
static void trim(char *s) {
    if (!s) return;
    int l = strlen(s);
    while (l > 0 && (s[l-1] == '\n' || s[l-1] == '\r' || s[l-1] == ' ' || s[l-1] == '\t' || s[l-1] == ',')) s[--l] = '\0';
    char *p = s;
    while (*p == ' ' || *p == '\t') p++;
    if (p != s) memmove(s, p, strlen(p)+1);
}

/* retorna o texto entre as primeiras aspas encontradas (primeiro par) */
static int get_first_quoted(const char *line, char *out, int outsize) {
    const char *p = strchr(line, '"');
    if (!p) return 0;
    p++;
    const char *q = strchr(p, '"');
    if (!q) return 0;
    int len = (int)(q - p);
    if (len >= outsize) len = outsize - 1;
    strncpy(out, p, len);
    out[len] = '\0';
    return 1;
}

/* pega a string entre aspas que aparece após o caracter ':' (ex: "Professor": "samuel") */
static int get_quoted_after_colon(const char *line, char *out, int outsize) {
    const char *colon = strchr(line, ':');
    if (!colon) return 0;
    const char *p = strchr(colon, '"');
    if (!p) return 0;
    p++;
    const char *q = strchr(p, '"');
    if (!q) return 0;
    int len = (int)(q - p);
    if (len >= outsize) len = outsize - 1;
    strncpy(out, p, len);
    out[len] = '\0';
    return 1;
}

/* tenta ler um número float da linha (ex: "   6.0," ou "6.0") */
static int parse_float_from_line(const char *line, float *out) {
    double tmp;
    if (sscanf(line, " %lf", &tmp) == 1) {
        *out = (float)tmp;
        return 1;
    }
    return 0;
}

/* Carrega JSON (estruturado por matéria como no seu exemplo) */
void carregarJSON(const char *arquivo) {
    FILE *f = fopen(arquivo, "r");
    if (!f) { fprintf(stderr, "Erro: não foi possível abrir %s\n", arquivo); exit(1); }

    char linha[512];
    Materia *m = NULL;
    Aluno *a = NULL;

    while (fgets(linha, sizeof(linha), f)) {
        trim(linha);
        if (strlen(linha) == 0) continue;

        /* início de matéria: "NomeDaMateria": {  */
        if (strstr(linha, "\": {") || strstr(linha, "\":{")) {
            if (totalMaterias >= MAX_MATERIAS) continue;
            m = &materias[totalMaterias++];
            m->totalAlunos = 0;
            if (!get_first_quoted(linha, m->nome, sizeof(m->nome))) strcpy(m->nome, "SEM_NOME");
            m->professor[0] = '\0';
            a = NULL;
            continue;
        }

        /* dentro de materia */
        if (m != NULL) {
            /* Professor (pode ser "Professor") */
            if (strstr(linha, "\"Professor\"") || strstr(linha, "'Professor'")) {
                char tmp[100];
                if (get_quoted_after_colon(linha, tmp, sizeof(tmp))) {
                    strncpy(m->professor, tmp, sizeof(m->professor)-1);
                    m->professor[sizeof(m->professor)-1] = '\0';
                } else m->professor[0] = '\0';
                continue;
            }

            /* Início de um aluno (linha contendo "Nome": ) */
            if (strstr(linha, "\"Nome\"") || strstr(linha, "'Nome'")) {
                if (m->totalAlunos >= MAX_ALUNOS) { a = NULL; continue; }
                a = &m->alunos[m->totalAlunos++];
                a->nome[0] = a->turma[0] = a->ra[0] = '\0';
                a->notas[0]=a->notas[1]=a->notas[2]=a->notas[3]=0.0f;
                char tmp[200];
                if (get_quoted_after_colon(linha, tmp, sizeof(tmp))) strncpy(a->nome, tmp, sizeof(a->nome)-1);
                continue;
            }

            /* Turma */
            if (a != NULL && (strstr(linha, "\"Turma\"") || strstr(linha, "'Turma'"))) {
                char tmp[40];
                if (get_quoted_after_colon(linha, tmp, sizeof(tmp))) strncpy(a->turma, tmp, sizeof(a->turma)-1);
                continue;
            }

            /* RA */
            if (a != NULL && (strstr(linha, "\"RA\"") || strstr(linha, "'RA'"))) {
                char tmp[60];
                if (get_quoted_after_colon(linha, tmp, sizeof(tmp))) strncpy(a->ra, tmp, sizeof(a->ra)-1);
                continue;
            }

            /* Nota(s) — pode estar tudo em uma linha ou em várias linhas */
            if (a != NULL && (strstr(linha, "\"Nota\"") || strstr(linha, "\"Notas\"") || strstr(linha, "'Nota'"))) {
                /* caso: "Nota": [ 6.0, 9.0, 10.0, 2.0 ] all in one line */
                if (strchr(linha, '[') && strchr(linha, ']')) {
                    float v[4] = {0,0,0,0};
                    int cnt = sscanf(linha, "%*[^[] [ %f , %f , %f , %f", &v[0], &v[1], &v[2], &v[3]);
                    for (int k = 0; k < 4; k++) a->notas[k] = v[k];
                    (void)cnt;
                }
                /* caso: "Nota": [  \n 6.0, \n 9.0, \n ... \n ]  */
                else if (strchr(linha, '[')) {
                    int idx = 0;
                    while (idx < 4 && fgets(linha, sizeof(linha), f)) {
                        trim(linha);
                        if (strchr(linha, ']')) {
                            float v;
                            if (parse_float_from_line(linha, &v)) a->notas[idx++] = v;
                            break;
                        } else {
                            float v;
                            if (parse_float_from_line(linha, &v)) a->notas[idx++] = v;
                        }
                    }
                    while (idx < 4) a->notas[idx++] = 0.0f;
                } else {
                    /* linha contém "Nota" mas não '[', tenta ler próxima */
                    if (fgets(linha, sizeof(linha), f)) {
                        trim(linha);
                        if (strchr(linha, '[')) {
                            int idx = 0;
                            while (idx < 4 && fgets(linha, sizeof(linha), f)) {
                                trim(linha);
                                if (strchr(linha, ']')) {
                                    float v;
                                    if (parse_float_from_line(linha, &v)) a->notas[idx++] = v;
                                    break;
                                } else {
                                    float v;
                                    if (parse_float_from_line(linha, &v)) a->notas[idx++] = v;
                                }
                            }
                            while (idx < 4) a->notas[idx++] = 0.0f;
                        }
                    }
                }
                continue;
            }
        } /* fim if m != NULL */
    } /* fim while */

    fclose(f);
}

/* calcula média */
static float media_aluno(const Aluno *a) {
    return (a->notas[0] + a->notas[1] + a->notas[2] + a->notas[3]) / 4.0f;
}

/* listar matérias numeradas */
static void listarMaterias() {
    printf("\nMatérias disponíveis:\n");
    for (int i = 0; i < totalMaterias; i++) {
        printf("%2d - %s (Prof: %s) [alunos: %d]\n", i+1, materias[i].nome,
               materias[i].professor[0] ? materias[i].professor : "—",
               materias[i].totalAlunos);
    }
}


/* mostrar matéria por índice */
void mostrarMateria(char *materia) {
    for (int i = 0; i < totalMaterias; i++) {
        if (strcmp(materias[i].nome, materia) == 0) {

            printf("\n" BOLD CYAN "=============================================\n" RESET);
            printf(BOLD "              %s\n" RESET, materias[i].nome);
            printf("       Professor: %s\n", materias[i].professor);
            printf(BOLD CYAN "=============================================\n" RESET);

            printf(BOLD "Aluno                     Turma   RA         N1   N2   N3   N4   Média   Situação\n" RESET);
            printf("--------------------------------------------------------------------------------\n");

            for (int j = 0; j < materias[i].totalAlunos; j++) {
                Aluno *a = &materias[i].alunos[j];
                float m = media_aluno(a);

                const char *status = (m >= 6) ? GREEN "✅ APROVADO" RESET : RED "❌ REPROVADO" RESET;

                printf("%-24s %-7s %-9s  %.1f  %.1f  %.1f  %.1f   %.1f   %s\n",
                    a->nome, a->turma, a->ra,
                    a->notas[0], a->notas[1], a->notas[2], a->notas[3],
                    m, status
                );
            }
            return;
        }
    }
    printf(RED "Matéria não encontrada.\n" RESET);
}


/* buscar por RA */
void buscarRA(char *ra) {

    printf("\n" BOLD CYAN "================ BOLETIM ==================\n" RESET);
    printf(BOLD "RA: %s\n" RESET, ra);
    printf(CYAN "-------------------------------------------" RESET "\n");

    int encontrado = 0;

    printf(BOLD "Matéria               N1   N2   N3   N4   Média   Situação\n" RESET);
    printf("----------------------------------------------------------\n");

    for (int i = 0; i < totalMaterias; i++) {
        for (int j = 0; j < materias[i].totalAlunos; j++) {
            Aluno *a = &materias[i].alunos[j];
            if (strcmp(a->ra, ra) == 0) {
                encontrado = 1;
                float m = media_aluno(a);
                const char *status = (m >= 6) ? GREEN "✅ APROVADO" RESET : RED "❌ REPROVADO" RESET;

                printf("%-20s %.1f  %.1f  %.1f  %.1f   %.1f   %s\n",
                    materias[i].nome,
                    a->notas[0], a->notas[1], a->notas[2], a->notas[3],
                    m, status
                );
            }
        }
    }

    if (!encontrado)
        printf(RED "\nRA não encontrado.\n" RESET);
}


/* main */
int main(void) {
    setlocale(LC_ALL, "");
    carregarJSON("materias.json"); // nome do arquivo (mude se preciso)

    if (totalMaterias == 0) {
        printf("Nenhuma matéria carregada. Verifique o arquivo materias.json e o formato.\n");
        return 0;
    }

    int opc;
    char buf[128];

    while (1) {
        printf("\n\n======= SMARTCLASS =======\n");
        printf("\n\n===== MENU =====\n");
        printf("1 - Listar matérias\n");
        printf("2 - Visualizar matéria (por número)\n");
        printf("3 - Buscar boletim por RA\n");
        printf("4 - Sair\n");
        printf("Escolha: ");
        if (scanf("%d", &opc) != 1) { scanf("%*s"); printf("Entrada inválida.\n"); continue; }

        switch (opc) {
            case 1:
                listarMaterias();
                break;
            case 2:
                listarMaterias();
                printf("Digite o número da matéria: ");
                if (scanf("%d", &opc) != 1) { scanf("%*s"); printf("Entrada inválida.\n"); break; }
                if (opc >= 1 && opc <= totalMaterias)
                    mostrarMateria(materias[opc - 1].nome);
                else
                    printf(RED "Número inválido!\n" RESET);

                break;
            case 3:
                printf("Digite o RA do aluno: ");
                scanf(" %127s", buf);
                buscarRA(buf);
                break;
            case 4:
                printf("Saindo...\n");
                return 0;
            default:
                printf("Opção inválida.\n");
        }
    }

    return 0;
}
