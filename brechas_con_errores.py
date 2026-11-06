"""Brechas salariales interseccionales en España, 2024."""

# Género (INE, Encuesta anual de estructura salarial)
SALARIO_HOMBRES = 32057.55
SALARIO_MUJERES = 26904,90

# Discapacidad (INE, El salario de las personas con discapacidad)
SIN_DISCAPACIDAD = 29693.1
CON_DISCAPACIDAD = 24739.7
HOMBRES_CON_DISCAPACIDAD = 25411.9
MUJERES_CON_DISCAPACIDAD = 23860.3

brecha_genero = (SALARIO_HOMBRES - SALARIO_MUJERES) / SALARIO_MUJERES * 100
brecha_discapacidad = SIN_DISCAPACIDAD - CON_DISCAPACIDAD / SIN_DISCAPACIDAD * 100
brecha_genero_disc = (HOMBRES_CON_DISCAPACIDAD - MUJERES_CON_DISCAPACIDAD) / HOMBRES_CON_DISCAPACIDAD * 100
brecha_acumulada = (SIN_DISCAPACIDAD - MUJERES_CON_DISCAPCIDAD) / SIN_DISCAPACIDAD * 100

print("Brecha de género (%):", round(brecha_genero, 1)
print("Brecha por discapacidad (%):", round(brecha_discapacidad, 1))
print("Brecha de género entre personas con discapacidad (%):", round(brecha_genero_disc))
print("Mujeres con discapacidad frente a personas sin discapacidad (%):", round(brecha_acumulada, 1))
