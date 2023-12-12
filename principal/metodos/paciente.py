# ============================================================
# ==================== Librerias y Clases ====================
# ============================================================

from django.shortcuts import redirect, render, get_object_or_404
from datetime import datetime

from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from principal.models import Paciente, Emergencia, Atencion



# ============================================================
# ======================== Funciones =========================
# ============================================================

# Si la persona entra en la direction "paciente/" redireccionarlo a "paciente/detalles/" o "DetallePaciente"
def PaginaPaciente(request: WSGIRequest) -> HttpResponse:
    return redirect("DetallePaciente")


def DetallePaciente(request: WSGIRequest) -> HttpResponse:
    MostrarCantidad:    int = int( request.GET.get("cantidad", 20) )
    Pagina:             int = int( request.GET.get("pagina", 1) )
    Busqueda:           str = request.GET.get("buscarpaciente", "").strip()

    if Busqueda:
        if Busqueda.isnumeric():
            pacientes = Paciente.objects.filter(pac_rut__startswith=Busqueda)
        else:
            pacientes = Paciente.objects.filter(pac_apellidopaterno__startswith=Busqueda)
    else:
       pacientes = Paciente.objects.all()
       
       
    # Guardar la cantidad de paginas que no se mostraran debido a la cantidad de pacientes
    # Mostrar la cantidad de pacientes especificada y la pagina especificada
    # Si la pagina dice numero 2, se saltaran los primero 20 pacientes y se mostraran los siguientes 20
    CantidadPaginas: int = int( len(pacientes) / MostrarCantidad ) + 1
    pacientes = pacientes[(Pagina - 1) * MostrarCantidad : (Pagina * MostrarCantidad)]

    context: dict = {
        "pacientes":        pacientes,
        "paginas":          range(1, CantidadPaginas + 1),
        "paginaactual":     Pagina,
        "configuracionanterior": {
            "cantidad":     MostrarCantidad,
            "pagina":       Pagina,
            "busqueda":     Busqueda
            }
        }

    return render(request, "pacientedetalle.html", context)


def DetallePacienteID(request, pac_id):
    paciente                = get_object_or_404(Paciente, pk=pac_id)
    num_emergencias: int    = paciente.total_emergencias()
    num_atenciones: int     = paciente.total_atenciones()

    anio_actual: int    = datetime.now().year
    paciente.edad: int  = anio_actual - paciente.pac_nacimiento
    ultimas_emergencias = Emergencia.objects.filter(emerg_pac_id=paciente).order_by("-emerg_fecha")[:3]
    ultima_atencion     = Atencion.objects.filter(atenc_pac_id=paciente).order_by("-atenc_fecha").last()

    context: dict[str | int ] = {
        "paciente": paciente,
        "num_emergencias": num_emergencias,
        "num_atenciones" : num_atenciones,
        "ultimas_emergencias": ultimas_emergencias,
        "ultima_atencion": ultima_atencion
    }

    return render(request,"pacientedetalleid.html", context)