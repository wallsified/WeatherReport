# Estilo de Documentación del Código

## Generalidades

- La documentación se hace usando comillas triples `""" documentacion """`.
- Las cadenas de documentación se colocan inmediatamente después de la clase o método de clase con sangría de un nivel.
- Los espacios que se están dejando entre la ubicación de la documentación y en donde inicia el código son necesarios. Inducen una buena práctica.
- Es válido el uso de tags como `TODO:, BUG:, FIXME:` en forma de comentarios siempre y cuando se explique la razón.
- El nombre de las variables debe de seguir `snake_case`, ya que es lo indicado por las normas PEP de Python

```python
class clase_simple:
    """Documentación de la clase"""
		
		# TODO: Hacer la documentacion!
    def say_hello(self, name: str):
        """Documentación del método."""

        print(f'Hello {name}')
```

## Documentar Clases

Las cadenas de documentación de clase deben contener la siguiente información:

- Un breve resumen de su finalidad y comportamiento.
- Cualquier método público, junto con una breve descripción.
- Cualquier propiedad de clase (atributos)
- El nombre de usuario de quien haya creado la clase

Los parámetros del constructor de la clase deben documentarse dentro de la cadena de documentación del método de clase `_**init_**`. Los métodos individuales deben documentarse utilizando sus cadenas de documentación individuales. 

```python
class Animal:
    """
   Aqui la descripción de lo que hace la clase

    ...

    Atributos de la clase
    ----------
    propiedad1 : tipo

    Métodos
    -------
    método(Parámetro(s))
        Descripción rápida del método

		Autor(es)
		-------
		@suArrobaEnGithub		
    """
```

## Documentar Métodos

Las cadenas de documentación del método (sea o no de clase) deben contener lo siguiente:

- Una breve descripción de qué es el método y para qué se utiliza.
- Cualquier argumento (tanto obligatorio como opcional) que se pase, incluidos los argumentos de palabras clave.
- Etiquetar cualquier argumento que se considere opcional o que tenga un valor predeterminado
- Cualquier efecto secundario que ocurra al ejecutar el método.
- Cualquier excepción que se plantee
- Cualquier restricción sobre cuándo se puede llamar al método.
- En caso de que el método creado sea por una persona diferente a la creadora de la clase, se anota el nombre de la misma forma explicada arriba. Si no, se omite.

```python
def says(self, algo=None):
        """Resumen del método en una linea .

        Aqui explicamos con más detalle de ser necesario

        Parámetros
        ----------
        algo : str, optional
            Descripción del parámetro (Descripción de valor predeterminado)

        Excepciones
        ------
        NotImplementedError
            Explicación sobre la excepcion

				Autor(es)
				-------
				@suArrobaEnGithub		
        """
```

## Documentar `imports`

En este caso, al no existir una manera oficial de hacerlo, basta con explicarlo con comentarios normales. Sin embargo, es necesario notar que las normas *****PEP***** indican que no sean más de 72 caracteres en la linea en cuestión a documentar. 

```python
# Esto será suficiente mientras que explique se importa
from algunaCosa import algoEspecifico
```
