#header "res\test.head.json"

out vec4 FragColor;


float mandelbrot(in vec2 c)
{
    float rsq = uRadius * uRadius;
    
    vec2 z = vec2(0);
    float s = 0.0;
    
    for (int i = 0; i < 512; i++) {
        z = vec2(z.x*z.x - z.y*z.y, 2 * z.x * z.y) + c;
        if (dot(z, z) > rsq)
            break;
        s += 1.0;
    }
    
    return s / 512.0;
}


void main()
{
    vec2 uv = 2.0 * (gl_FragCoord.xy - 0.5 * uResolution) / uResolution.y;
    vec2 mp = -uMousePos / uResolution;
    
    float col = mandelbrot(uv / uZoom + mp);
    
    FragColor = vec4(vec3(col), 1.0);
}