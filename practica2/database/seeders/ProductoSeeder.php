<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Producto; // Importante: Importamos el modelo

class ProductoSeeder extends Seeder
{
    public function run(): void
    {
        // Producto 1
        Producto::create([
            'nombre' => 'Laptop Gamer',
            'descripcion' => 'Laptop rápida para juegos y diseño',
            'precio' => 1500.00
        ]);

        // Producto 2
        Producto::create([
            'nombre' => 'Mouse Inalámbrico',
            'descripcion' => 'Mouse ergonómico con batería recargable',
            'precio' => 25.50
        ]);

        // Producto 3
        Producto::create([
            'nombre' => 'Teclado Mecánico',
            'descripcion' => 'Teclado con luces RGB configurables',
            'precio' => 80.00
        ]);
    }
}