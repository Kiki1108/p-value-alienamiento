import subprocess
import tempfile
import random
import matplotlib.pyplot as plt

secuencia_a = 'GCTAATCAGTGCATCGATCT'
secuecnia_b = 'GTTGACATCTGCATGCTAGA'

# Generar 10,000 secuencias al azar de 20 bases
bases = ['A', 'C', 'G', 'T']
secuencias_azar = [''.join(random.choices(bases, k=20)) for _ in range(1000)]
# Ahora secuencias_azar contiene las secuencias aleatorias

# Guardar las secuencias en archivos FASTA temporales
def write_fasta(seq, name):
    f = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.fasta')
    f.write(f'>{name}\n{seq}\n')
    f.close()
    return f.name

seq_a = write_fasta(secuencia_a, 'seq1')
seq_b = write_fasta(secuecnia_b, 'seq2')

# Ejecutar needle
def run_needle(fasta1, fasta2, outfile):
    cmd = [
        'needle',
        '-asequence', fasta1,
        '-bsequence', fasta2,
        '-gapopen', '10',
        '-gapextend', '0.5',
        '-outfile', outfile
    ]
    subprocess.run(cmd, check=True)

output_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt').name
run_needle(seq_a, seq_b, output_file)

# Leer y mostrar el resultado y extraer el score
score = None
with open(output_file) as f:
    content = f.read()
    print(content)
    for line in content.splitlines():
        if line.startswith('# Score:'):
            score = float(line.split()[-1])
            break
print('Score del alineamiento:', score)

# Evaluar cada secuencia aleatoria contra secuencia_b y guardar los scores
scores_azar = []
# Crear archivo fasta de secuencia_b solo una vez
seq_b_fasta = write_fasta(secuecnia_b, 'seq_b')
for i, seq in enumerate(secuencias_azar):
    seq_a_fasta = write_fasta(seq, f'seq_azar_{i}')
    temp_out = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt').name
    run_needle(seq_a_fasta, seq_b_fasta, temp_out)
    score = None
    with open(temp_out) as f:
        for line in f:
            if line.startswith('# Score:'):
                score = float(line.split()[-1])
                break
    scores_azar.append(score)

# Ahora scores_azar contiene los scores de cada alineamiento
print('Primeros 10 scores de secuencias al azar:', scores_azar[:100])

# Graficar histograma de los scores
plt.hist(scores_azar, bins=100, edgecolor='black')
plt.xlabel('Score de alineamiento')
plt.ylabel('Frecuencia')
plt.title('Histograma de scores de alineamiento (secuencias al azar vs secuencia_b)')
plt.show()

