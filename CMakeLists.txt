# CMakeList.txt: projeto de CMake para crypto, incluir fonte e definir
# lógica específica a um projeto aqui.
#
cmake_minimum_required (VERSION 3.8)

set (CMAKE_CXX_STANDARD 17)

# Adicione a fonte ao executável deste projeto.
add_executable (crypto "crypto.cpp" "crypto.h")
# TODO: Adicione testes e instale destinos, se necessário.
