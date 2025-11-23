<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class PaginaController extends Controller
{
    // Requisito: Método invocado por la ruta de bienvenida 
    public function bienvenida() {
        // Retorna la vista estática con el mensaje 
        return view('bienvenida');
    }

    // Requisito: Método que captura el parámetro nombre de la URL 
    public function saludo($nombre) {
        // Pasa el dato capturado a la vista 'saludo' 
        return view('saludo', ['nombre' => $nombre]);
    }
}