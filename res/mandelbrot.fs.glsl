#header "res\mandelbrot.head.json"

out vec4 FragColor;


float mandelbrot(in vec2 c)
{
    float rsq = uRadius * uRadius;
    
    vec2 z = vec2(0);
    float s = -1.0;
    
    for (int i = 0; i < uIters; i++) {
        z = vec2(z.x*z.x - z.y*z.y, 2 * z.x * z.y) + c;
        if (dot(z, z) > rsq)
        {
            s = float(i);
            break;
        }
        //s += 1.0;
    }
    
    return s;
}

void main()
{
    vec2 uv = 2.0 * (gl_FragCoord.xy - 0.5 * uResolution) / uResolution.y;
    vec2 mp = -uMousePos / uResolution;
    
    float l = mandelbrot(uv / uZoom + mp);

    vec3 col = 0.5 + 0.5*sin(vec3(2.5, 2.1, 1.5) + l * uGamma);

    if (l < 0.0)
        col = vec3(0, 0, 0);
    
    FragColor = vec4(col, 1.0);
}