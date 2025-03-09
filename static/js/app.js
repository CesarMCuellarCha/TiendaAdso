
function mostrarImagen(evento){
    const archivos = evento.target.files
    const archivo = archivos[0]
    const url = URL.createObjectURL(archivo)  
    document.getElementById("imagenProducto").src=url
  }

  function eliminar(id){
    alert(id)
    Swal.fire({
      title: 'Eliminar Producto',
      text: "¿Está seguro de eliminar?",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      cancelButtonText: 'NO',
      confirmButtonText: 'SI'
    }).then((result) => {
      if (result.isConfirmed) {
         location.href="/eliminar/"+id
      }
    })
  }

