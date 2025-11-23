<?php

use Illuminate\Support\Facades\Route;
// ESTA ES LA LÍNEA QUE FALTABA:
use App\Http\Controllers\ProductoController;

Route::get('/', function () {
    return view('welcome');
});

// Ruta para ver el catálogo
Route::get('/productos', [ProductoController::class, 'index']);