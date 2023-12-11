class InString:
    name = 'in_string'
    def code(self):
        label_copy = 'paco45'#NameLabel('copy_in').get()
        length =  'jisus12'#NameLabel('length_in_string').get()

        return [
        'in_string:',
        'li $v0, 8',
        'la $a0, string_space',
        'li $a1, 1024',
        'syscall',

        '\tmove $t0, $a0',        #mueve a t0 el valor donde esta almacenado el string
        '\taddi $t1, $zero, -1',  #Guarda -1 en t1
        f'\t{length}:',
        '\tlb $t2, 0($t0)',       # Cargar en t2 el caracter actual
        '\taddi $t0, $t0, 1',         #  aunmenta t0 en 1
        '\taddi $t1, $t1, 1',         # aumenta t1 en 1, que seria el contador del len 
        f'\tbnez $t2, {length}',  # lo compara con el caracter nulo, en caso de no serlo repite el ciclo
        '\tmove $t3, $t1',        # mueve a $t3 el valor de $t1, t3 es entonces el valor de length-1        
        
        'addi $t3, $t0, -2',
        'sb $zero, 0($t3)',      #En la posicion de #t3, esta es la posicion del ultimo caracter del string sin contar el nulo
        
        'move $t0, $a0',         #t0 tiene la direccion del string ahora
        'addi $a0, $t1, 1',      # espacio para guardar el string que se entra
        'li $v0, 9',             # Código de sistema para sbrk
        'syscall',               
        'move $t1, $v0',
        f'{label_copy}:',
        'lb $t3, 0($t0)',             #carga byte de t0
        'sb $t3, 0($t1)',              #guarda el byte en t1
        'addi $t0, $t0, 1',              #aumenta t0 en 1
        'addi $t1, $t1, 1',              #aumenta t1 en 1
        f'\tbnez $t3, {label_copy}',  # lo compara con el caracter nulo, en caso de no serlo repite el ciclo
        'move $a0, $v0', 

        '\tjr $ra'              
        ]
  # Leer el string ingresado por el usuario



a=InString()
with open("zin_str.s", "w") as f:
    f.write("\n".join(a.code()))
