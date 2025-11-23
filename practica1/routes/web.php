<?php

use Illuminate\Support\Facades\Route;
// Importante: Llamamos al controlador que creaste
use App\Http\Controllers\PaginaController;

Route::get('/', function () {
    return view('welcome');
});

// Requisito 1: Ruta estática '/bienvenida' [cite: 12]
Route::get('/bienvenida', [PaginaController::class, 'bienvenida']);

// Requisito 2: Ruta dinámica '/saludo/{nombre}' [cite: 16]
Route::get('/saludo/{nombre}', [PaginaController::class, 'saludo']);