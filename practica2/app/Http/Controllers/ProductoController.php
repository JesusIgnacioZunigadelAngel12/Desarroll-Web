<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Producto; // Importamos tu modelo

class ProductoController extends Controller
{
    public function index() {
        // Consultar todos los productos de la BD
        $productos = Producto::all();
        
        // Retornar la vista pasando los datos
        return view('productos', ['productos' => $productos]);
    }
}