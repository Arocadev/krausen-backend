from sqlalchemy.orm import Session
from app.models.ingrediente import Ingrediente

INGREDIENTES_INICIALES = [
    # Maltas
    {"nombre": "Malta Pilsner", "tipo": "malta"},
    {"nombre": "Malta Pale Ale", "tipo": "malta"},
    {"nombre": "Malta Viena", "tipo": "malta"},
    {"nombre": "Malta Munich", "tipo": "malta"},
    {"nombre": "Malta Caramelo", "tipo": "malta"},
    {"nombre": "Malta Chocolate", "tipo": "malta"},
    {"nombre": "Malta Negra", "tipo": "malta"},
    {"nombre": "Malta Trigo", "tipo": "malta"},
    {"nombre": "Malta Avena", "tipo": "malta"},
    {"nombre": "Malta Centeno", "tipo": "malta"},
    {"nombre": "Malta Ahumada", "tipo": "malta"},
    {"nombre": "Malta Crystal", "tipo": "malta"},
    # Lúpulos
    {"nombre": "Lúpulo Cascade", "tipo": "lupulo"},
    {"nombre": "Lúpulo Centennial", "tipo": "lupulo"},
    {"nombre": "Lúpulo Chinook", "tipo": "lupulo"},
    {"nombre": "Lúpulo Citra", "tipo": "lupulo"},
    {"nombre": "Lúpulo Saaz", "tipo": "lupulo"},
    {"nombre": "Lúpulo Hallertau", "tipo": "lupulo"},
    {"nombre": "Lúpulo Fuggle", "tipo": "lupulo"},
    {"nombre": "Lúpulo Simcoe", "tipo": "lupulo"},
    {"nombre": "Lúpulo Amarillo", "tipo": "lupulo"},
    {"nombre": "Lúpulo Mosaic", "tipo": "lupulo"},
    {"nombre": "Lúpulo Galaxy", "tipo": "lupulo"},
    {"nombre": "Lúpulo Nelson Sauvin", "tipo": "lupulo"},
    # Levaduras
    {"nombre": "Levadura Ale Americana", "tipo": "levadura"},
    {"nombre": "Levadura Ale Inglesa", "tipo": "levadura"},
    {"nombre": "Levadura Lager", "tipo": "levadura"},
    {"nombre": "Levadura Belga", "tipo": "levadura"},
    {"nombre": "Levadura Weizen", "tipo": "levadura"},
    {"nombre": "Levadura Saison", "tipo": "levadura"},
    {"nombre": "Levadura Kveik", "tipo": "levadura"},
    # Adjuntos
    {"nombre": "Agua", "tipo": "adjunto"},
    {"nombre": "Azúcar de caña", "tipo": "adjunto"},
    {"nombre": "Miel", "tipo": "adjunto"},
    {"nombre": "Naranja", "tipo": "adjunto"},
    {"nombre": "Limón", "tipo": "adjunto"},
    {"nombre": "Cilantro", "tipo": "adjunto"},
    {"nombre": "Jengibre", "tipo": "adjunto"},
    {"nombre": "Canela", "tipo": "adjunto"},
    {"nombre": "Vainilla", "tipo": "adjunto"},
    {"nombre": "Café", "tipo": "adjunto"},
    {"nombre": "Cacao", "tipo": "adjunto"},
    {"nombre": "Frambuesa", "tipo": "adjunto"},
    {"nombre": "Cereza", "tipo": "adjunto"},
    {"nombre": "Mango", "tipo": "adjunto"},
    {"nombre": "Maracuyá", "tipo": "adjunto"},
    {"nombre": "Avena en copos", "tipo": "adjunto"},
    {"nombre": "Lactosa", "tipo": "adjunto"},
]

def seed_ingredientes(db: Session):
    for item in INGREDIENTES_INICIALES:
        existe = db.query(Ingrediente).filter(Ingrediente.nombre == item["nombre"]).first()
        if not existe:
            db.add(Ingrediente(nombre=item["nombre"], tipo=item["tipo"]))
    db.commit()
    print(f"✅ Ingredientes cargados correctamente")