<!DOCTYPE html>
<html>
<head>
    <title>Lista de Productos</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .tarjeta { 
            border: 1px solid #ccc; 
            padding: 15px; 
            margin-bottom: 10px; 
            border-radius: 8px; 
            background-color: #f9f9f9;
        }
        h2 { margin-top: 0; color: #2c3e50; }
        .precio { color: #27ae60; font-weight: bold; font-size: 1.2em; }
    </style>
</head>
<body>
    <h1>Catálogo de Productos</h1>

    @foreach ($productos as $producto)
        <div class="tarjeta">
            <h2>{{ $producto->nombre }}</h2>
            <p>{{ $producto->descripcion }}</p>
            <p class="precio">Precio: ${{ $producto->precio }}</p>
        </div>
    @endforeach

</body>
</html>