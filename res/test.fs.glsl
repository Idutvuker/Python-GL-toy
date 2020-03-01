#version 330 core

uniform ivec2 uResolution;

out vec4 FragColor;

void main()
{
    vec2 uv = gl_FragCoord.xy / uResolution;
    
    FragColor = vec4(uv, 0.0, 1.0);
}