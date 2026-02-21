"""
Script de datos de prueba: 100 clientes + mascotas + productos veterinarios
Ejecutar desde la carpeta backend con el venv activo:
  python seed_data.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.config.database import SessionLocal, engine, Base
from src.models.cliente import Cliente
from src.models.mascota import Mascota
from src.models.producto import Producto
from src.models.usuario import Usuario
from src.models.venta import Venta, DetalleVenta
import random, bcrypt

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ──────────────────────────────────────────────
# PRODUCTOS VETERINARIOS (60 productos)
# ──────────────────────────────────────────────
productos_data = [
  # ALIMENTOS PERRO
  ("ALI-P001","Royal Canin Adult Maxi 15kg","Alimento balanceado para perros adultos razas grandes","Alimento",85.50,40,8),
  ("ALI-P002","Pedigree Adulto Carne 20kg","Alimento completo para perros adultos","Alimento",55.00,50,10),
  ("ALI-P003","Hills Science Diet Adulto 12kg","Premium nutrición para perros adultos","Alimento",110.00,25,5),
  ("ALI-P004","Eukanuba Puppy Razas Grandes 15kg","Fórmula especial para cachorros","Alimento",95.00,20,5),
  ("ALI-P005","Proplan Sensitive Skin 13kg","Para perros con piel sensible","Alimento",105.00,18,4),
  ("ALI-P006","Purina Dog Chow Cachorros 8kg","Nutrición completa para cachorros","Alimento",42.00,35,8),
  ("ALI-P007","Royal Canin Chihuahua Adult 1.5kg","Diseñado para Chihuahuas adultos","Alimento",22.00,30,6),
  ("ALI-P008","Acana Perros Adultos 11.4kg","Alimento sin granos con proteína fresca","Alimento",135.00,15,3),
  # ALIMENTOS GATO
  ("ALI-G001","Royal Canin Indoor Adult 4kg","Para gatos de interior","Alimento",38.00,35,7),
  ("ALI-G002","Whiskas Adulto Carne 10kg","Sabor a carne para gatos adultos","Alimento",45.00,40,8),
  ("ALI-G003","Hills Science Diet Gato 4kg","Premium para gatos adultos","Alimento",52.00,22,5),
  ("ALI-G004","Purina One Sensitive 3kg","Para gatos con estómagos sensibles","Alimento",35.00,28,6),
  ("ALI-G005","Proplan Kitten 1.5kg","Nutrición para gatitos hasta 12 meses","Alimento",28.00,25,5),
  ("ALI-G006","Fancy Feast Lata x12","Pack de latas gourmet variedad","Alimento",18.00,50,10),
  # MEDICAMENTOS
  ("MED-001","Drontal Plus Tabs x10","Antiparasitario interno para perros","Medicamento",24.50,60,12),
  ("MED-002","Frontline Plus Perros M x3","Antiparasitario externo antipulgas","Medicamento",28.00,45,10),
  ("MED-003","Frontline Plus Gatos x3","Antiparasitario externo para gatos","Medicamento",26.00,40,10),
  ("MED-004","Advocate Perros Grandes x3","Antiparasitario externo e interno","Medicamento",42.00,30,6),
  ("MED-005","Virbagen Omega Perro","Inmunomodulador para perros","Medicamento",65.00,15,4),
  ("MED-006","Tramadol 50mg x20","Analgésico veterinario","Medicamento",18.00,30,8),
  ("MED-007","Amoxicilina 500mg x20","Antibiótico de amplio espectro","Medicamento",12.00,40,10),
  ("MED-008","Metronidazol 250mg x20","Antiprotozoario y antibacteriano","Medicamento",9.50,35,8),
  ("MED-009","Prednisolona 20mg x20","Antiinflamatorio corticoide","Medicamento",11.00,25,6),
  ("MED-010","Cephalexin 500mg x20","Antibiótico cefalosporina","Medicamento",15.00,28,6),
  ("MED-011","Enrofloxacina 50mg x10","Antibiótico fluoroquinolona","Medicamento",14.00,30,6),
  ("MED-012","Meloxicam 1mg/ml 10ml","Antiinflamatorio AINE inyectable","Medicamento",22.00,20,5),
  ("MED-013","Suero Fisiológico 500ml","Solución isotónica para hidratación","Medicamento",6.50,80,20),
  ("MED-014","Vitamina C Inyectable 100mg/5ml","Suplemento vitamínico","Medicamento",8.00,40,10),
  ("MED-015","Omega 3 Perros x60 caps","Suplemento ácidos grasos","Medicamento",19.00,35,7),
  # VACUNAS
  ("VAC-001","Vacuna Polivalente Perro","Distemper, Parvovirus, Adenovirus","Vacuna",18.00,80,15),
  ("VAC-002","Vacuna Antirrábica Perro 1ml","Rabia para perros","Vacuna",12.00,100,20),
  ("VAC-003","Vacuna Antirrábica Gato 1ml","Rabia para gatos","Vacuna",12.00,80,15),
  ("VAC-004","Vacuna Triple Felina","Rinotraqueítis, Calicivirus, Panleucopenia","Vacuna",16.00,60,12),
  ("VAC-005","Vacuna Leptospirosis","Leptospira para perros","Vacuna",14.00,50,10),
  ("VAC-006","Vacuna Bordetella Intranasal","Tos de las perreras","Vacuna",20.00,30,6),
  # HIGIENE Y CUIDADO
  ("HIG-001","Shampoo Antipulgas Perro 500ml","Shampoo con piretrina natural","Higiene",15.50,50,10),
  ("HIG-002","Shampoo Avena Perro 500ml","Para piel sensible e irritada","Higiene",13.00,45,9),
  ("HIG-003","Shampoo Neutro Gato 350ml","Específico para la piel felina","Higiene",12.00,35,7),
  ("HIG-004","Cortaúñas Profesional","Acero inoxidable talla M","Higiene",9.00,40,8),
  ("HIG-005","Cepillo Dientes + Pasta x2","Kit higiene dental canina","Higiene",11.50,30,6),
  ("HIG-006","Limpiador de Oídos 100ml","Solución limpiadora auricular","Higiene",10.00,40,8),
  ("HIG-007","Colonia Perros Baby Powder 250ml","Perfume suave post-baño","Higiene",8.50,35,7),
  ("HIG-008","Toallitas Húmedas Perro x50","Para limpiezas rápidas","Higiene",6.00,60,12),
  # ACCESORIOS
  ("ACC-001","Correa Retráctil 5mt Talla M","Para perros hasta 25kg","Accesorio",18.00,30,6),
  ("ACC-002","Collar Antipulgas Seresto Perro","Protección 8 meses","Accesorio",45.00,25,5),
  ("ACC-003","Collar Antipulgas Seresto Gato","Protección 8 meses felinos","Accesorio",42.00,20,5),
  ("ACC-004","Arnés Regulable Talla S","Para perros pequeños","Accesorio",14.00,25,5),
  ("ACC-005","Cama Ortopédica M 60x80cm","Espuma viscoelástica","Accesorio",55.00,15,3),
  ("ACC-006","Transportadora Plástica #3","Para perros medianos y gatos grandes","Accesorio",48.00,12,3),
  ("ACC-007","Bebedero Automático 2L","Fuente de agua con filtro","Accesorio",32.00,18,4),
  ("ACC-008","Juguete Kong Classic Talla M","Juguete rellenable resistente","Accesorio",16.00,30,6),
  ("ACC-009","Plato Antiderrapante Acero","Doble uso comida y agua","Accesorio",7.50,40,8),
  ("ACC-010","Ropa Impermeable Perro Talla S","Chubasquero ajustable","Accesorio",22.00,20,5),
  ("ACC-011","Arena Silica Gel Gato 3.8L","Ultra absorbente sin polvo","Accesorio",18.00,40,8),
  ("ACC-012","Rascador Torre Gato","Sisal natural 120cm","Accesorio",65.00,10,2),
  ("ACC-013","GPS Collar Tracking","Rastreo GPS para mascotas","Accesorio",89.00,8,2),
  # OTROS
  ("OTR-001","Jeringa 5ml x10","Plástico estéril desechable","Otro",3.50,100,20),
  ("OTR-002","Guantes Látex Talla M x50","Guantes de examinación","Otro",7.00,80,15),
  ("OTR-003","Termómetro Digital Veterinario","Rectal de punta flexible","Otro",12.50,25,5),
  ("OTR-004","Puppy Training Pads x30","Pañales absorbentes entrenamiento","Otro",15.00,40,8),
  ("OTR-005","Microchip Kit Inyectable","Implante de identificación","Otro",28.00,30,6),
]

print("🔄 Insertando productos...")
prod_insertados = 0
for codigo, nombre, desc, cat, precio, stock, stock_min in productos_data:
    if not db.query(Producto).filter(Producto.codigo == codigo).first():
        db.add(Producto(codigo=codigo, nombre=nombre, descripcion=desc,
                        categoria=cat, precio=precio, stock=stock, stock_minimo=stock_min))
        prod_insertados += 1
db.commit()
print(f"  ✅ {prod_insertados} productos insertados")

# ──────────────────────────────────────────────
# CLIENTES Y MASCOTAS (100 clientes)
# ──────────────────────────────────────────────

nombres = ["Carlos","María","José","Ana","Luis","Laura","Miguel","Carmen","Jorge","Patricia",
           "Roberto","Gabriela","Fernando","Valentina","Andrés","Sofía","Ricardo","Isabella",
           "Diego","Daniela","Pablo","Camila","Sergio","Mariana","Alejandro","Lucía","Manuel",
           "Paula","Oscar","Sandra","Héctor","Natalia","Gustavo","Adriana","Rafael","Monica",
           "Javier","Claudia","Raúl","Verónica","Alberto","Beatriz","Ernesto","Teresa","César",
           "Lorena","Felipe","Alejandra","Víctor","Paola"]

apellidos = ["García","Rodríguez","López","Martínez","González","Pérez","Sánchez","Ramírez",
             "Torres","Flores","Rivera","Gómez","Díaz","Morales","Reyes","Cruz","Herrera",
             "Mendoza","Ruiz","Vargas","Castillo","Ortega","Jiménez","Medina","Aguilar",
             "Paredes","Vásquez","Gutiérrez","Castro","Ramos","Núñez","Salazar","Romero",
             "Alvarez","Suárez","Chávez","Espinoza","Carrillo","Delgado","Figueroa"]

razas_perro = ["Labrador Retriever","Golden Retriever","Bulldog Francés","Poodle","Beagle",
               "Rottweiler","Pastor Alemán","Chihuahua","Shih Tzu","Pomerania","Husky Siberiano",
               "Yorkshire Terrier","Dalmata","Boxer","Cocker Spaniel","Schnauzer","Maltés",
               "Bichón Frisé","Dachshund","Doberman","Sin raza definida"]

razas_gato = ["Persa","Maine Coon","Siamés","Ragdoll","British Shorthair","Bengalí",
              "Angora Turco","Abisinio","Esfinge","Scottish Fold","Sin raza definida"]

nombres_mascotas = ["Max","Bella","Charlie","Luna","Buddy","Lucy","Cooper","Daisy","Rocky",
                    "Molly","Jake","Sadie","Duke","Maggie","Teddy","Sophie","Bear","Chloe",
                    "Zeus","Lola","Milo","Zoe","Oreo","Nala","Simba","Coco","Leo","Kira",
                    "Thor","Maya","Diesel","Leia","Titan","Mia","Bruno","Nora","Rex","Elsa",
                    "Toby","Lily","Oscar","Stella","Beto","Nina","Pelusa","Canela","Negra",
                    "Blanco","Pinto","Café","Manchas","Princesa","Rey","Lady","Lord","Bolita"]

obs_list = [None, None, "Alergia al pollo", "Miedo a los ruidos fuertes",
            "Castrado", "Esterilizada", "Problema dental crónico",
            "Requiere dieta especial sin gluten", "Alergia a las pulgas",
            "Hipertensión controlada", "Diabetes tipo 1 controlada",
            "Vacunas al día", "Piel sensible", "Obesidad controlada",
            "Artritis leve", "Epilepsia controlada con medicación"]

print("🔄 Insertando 100 clientes con mascotas...")
cli_insertados = 0
masc_insertadas = 0
random.seed(42)

for i in range(100):
    nombre = random.choice(nombres)
    apellido1 = random.choice(apellidos)
    apellido2 = random.choice(apellidos)
    apellido = f"{apellido1} {apellido2}"
    num = 1000 + i
    doc = f"174{num:04d}{random.randint(0,9)}"
    email = f"{nombre.lower()}.{apellido1.lower()}{i}@email.com"
    tel = f"09{random.randint(10,99)}{random.randint(100000,999999)}"
    barrios = ["Norte","Sur","Centro","La Mariscal","Quitumbe","Cotocollao","Chillogallo",
               "Carapungo","Calderón","El Tingo","Tumbaco","Cumbayá","San Rafael","Sangolquí"]
    dir_ = f"Av. {random.choice(apellidos)} N{random.randint(10,99)}-{random.randint(10,99)}, {random.choice(barrios)}"

    # Evitar duplicados de documento/email
    if db.query(Cliente).filter(Cliente.documento == doc).first():
        doc = f"175{num:04d}{random.randint(0,9)}"
    if db.query(Cliente).filter(Cliente.email == email).first():
        email = f"cliente{i}_{random.randint(100,999)}@veterinaria.com"

    cliente = Cliente(nombre=nombre, apellido=apellido, telefono=tel,
                      email=email, documento=doc, direccion=dir_)
    db.add(cliente)
    db.flush()  # para obtener el id
    cli_insertados += 1

    # 1-3 mascotas por cliente
    n_mascotas = random.randint(1, 3)
    for j in range(n_mascotas):
        especie = random.choices(["Perro","Gato","Ave","Conejo","Hamster"],
                                  weights=[55,30,7,5,3])[0]
        if especie == "Perro":
            raza = random.choice(razas_perro)
        elif especie == "Gato":
            raza = random.choice(razas_gato)
        else:
            raza = None

        mascota = Mascota(
            nombre=random.choice(nombres_mascotas),
            especie=especie,
            raza=raza,
            edad=random.choice([1,1,2,2,3,3,4,5,6,7,8,9,10,11,12]),
            sexo=random.choice(["Macho","Hembra"]),
            color=random.choice(["Negro","Blanco","Café","Dorado","Gris","Naranja",
                                  "Tricolor","Manchado","Atigrado","Crema",None]),
            peso=round(random.uniform(1.5, 45.0), 1),
            observaciones=random.choice(obs_list),
            cliente_id=cliente.id
        )
        db.add(mascota)
        masc_insertadas += 1

db.commit()
print(f"  ✅ {cli_insertados} clientes insertados")
print(f"  ✅ {masc_insertadas} mascotas insertadas")
print("\n🎉 Seed completado exitosamente!")
db.close()
