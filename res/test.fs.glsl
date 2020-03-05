#version 330 core

uniform ivec2 uResolution;
uniform vec2 uMousePos;

out vec4 FragColor;

void main()
{
    vec2 uv = gl_FragCoord.xy / uResolution;
    vec2 mp = fract(uMousePos / uResolution);
    
    float c = length(uv - mp);
    
    FragColor = vec4(vec3(c), 1.0);
}