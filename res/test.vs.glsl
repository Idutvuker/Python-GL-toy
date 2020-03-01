#version 330 core

void main()
{
	int id = gl_VertexID;
    vec3 pos;
    if (id == 0)
        pos = vec3(-1, -1, 0);
    else if (id == 1)
        pos = vec3(-1, 1, 0);
    else if (id == 2)
        pos = vec3(1, 1, 0);
    else
        pos = vec3(1, -1, 0);

    gl_Position = vec4(pos, 1.0);
}