#Para calcular la convolución y establecer los rangos al graficar.
import numpy as np
#Para graficar.
import matplotlib.pyplot as plt

#Obtenemos las velocidades y densidades, 
#para cada 25 metros, dada una profundidad.
def obtener_medios(zona : tuple, z_0 : int = 25) -> list:
	n = zona[0]//z_0
	medios = [(zona[1], zona[2])]*n 
	return medios

#Conversión de unidades.
def gcm3_to_kgm3(densidad : float) -> float:
	return densidad*1000

#Calculo de coeficiente de reflexion entre dos medios.
def coeficiente_reflexion(densidad_1 : float, densidad_2 : float, velocidad_1 : float, velocidad_2 : float) -> float:
	dv1 = gcm3_to_kgm3(densidad_1)*velocidad_1
	dv2 = gcm3_to_kgm3(densidad_2)*velocidad_2
	return (dv2 - dv1) / (dv2 + dv1)

#Obtencion de todos los coeficientes de reflexion.
#A partir de unos medios, sus densidades y velocidades.
def obtener_coeficientes_reflexion(medios: list) -> list:
	coeficientes_R = []

	#zip agrupa los cada medio con su medio contiguo.
	for medio_1, medio_2 in zip(medios, medios[1:]):
		d1, v1 = medio_1
		d2, v2 = medio_2
		coeficientes_R.append(
			coeficiente_reflexion(d1, d2, v1, v2)
			)

	return coeficientes_R
	
#Graficamos los resultados, en partes.
def graficar_separadas(profundidades : np.arange, coeficientes_R : list, convolucion : np.array) -> None:
	#Establecemos la cantidad de sub-graficas.
	fig, (ax_orig, ax_mag) = plt.subplots(2, 1)
	
	#Titulos.
	ax_orig.set_title('Coeficiente de Reflexión X Profundidad')
	ax_mag.set_title('Convolución X Profundidad')
	
	#Nombres ejes horizontales.
	ax_orig.set_xlabel('Profundidad (metros)')
	ax_mag.set_xlabel('Profundidad (metros)')
	
	#Nombres ejes verticales.
	ax_orig.set_ylabel('Coeficiente de Reflexión')
	ax_mag.set_ylabel('Convolución')

	#Dibujamos las graficas, diferenciandolas con colores.
	ax_orig.vlines(profundidades, 0, coeficientes_R, 'b', label='Coeficiente de Reflexión')
	ax_orig.hlines(0, 0, profundidades[-1], 'b')
	#ax_orig.plot(profundidades,coeficientes_R, 'b')
	ax_mag.plot(profundidades, convolucion, color='r')
	
	#Ajusta las graficas en el marco, para que queden espaciadas.
	fig.tight_layout(pad=3)
	
	#Muestra las graficas.
	plt.show()

#Graficamos los resultados, juntos.	
def graficar_juntas(profundidades : np.arange, coeficientes_R : list, convolucion : np.array) -> None:
	#Establecemos el marco.
	fig = plt.figure()
	
	#Titulo.
	plt.title('Coeficiente de Reflexión y Convolución X Profundidad')
	
	#Nombre eje horizontal.
	plt.xlabel('Profundidad (metros)')
	
	#Nombre eje vertical.
	plt.ylabel('CR y Conv')
	
	#Dibujamos las graficas.
	plt.vlines(profundidades, 0, coeficientes_R, 'b', label='Coeficiente de Reflexión')
	plt.hlines(0, 0, profundidades[-1], 'b')
	plt.plot(profundidades, convolucion, 'r', label='Convolución')
	
	#Generamos una leyenda, para identificar las graficas.
	plt.legend()
	
	#Graficamos.
	plt.show()
	
#Si es el programa principal.
if __name__ == '__main__':

	ondicula = [0, -0.1, -0.5, -0.5, -0.1, 0.5, 1, 1, 0.5, -0.1, -0.5, -0.5, -0.1, 0]
	
	#Datos (profundidad<m>, velodidad<m/s>, densidad<gr/cm**3>)
	datos = (
				(125,1800, 2),
				(275, 2000, 2.2),
				(100, 1825, 2.05),
				(325, 2200, 2.25),
				(125, 3000, 2.5)
			)
			
	#Obtenemos los medios a procesar.
	medios = [medio for dato in datos 
						for medio in obtener_medios(dato)]
	
	#Obtenemos los coeficientes de reflectividad.
	coeficientes_R = obtener_coeficientes_reflexion(medios)
	
	#Calculamos la convolución.
	convolucion = np.convolve(ondicula, coeficientes_R, 'same')
	
	#Array de profundidades cada 25 metros [0, 25, 50,..]
	profundidades = np.arange(0, 25*(len(medios)-1), 25)
	
	#Graficamos y comparamos.
	graficar_separadas(profundidades, coeficientes_R, convolucion)
	graficar_juntas(profundidades, coeficientes_R, convolucion)
