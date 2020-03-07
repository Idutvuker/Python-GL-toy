#version 330 core

out vec4 FragColor;

uniform vec2 uMousePos;
uniform ivec2 uResolution;
uniform float uZoom = 1.0;
uniform float uAlpha = 700.0;
uniform float uBeta = 2.0;
uniform int uIters = 11;

const float iTime = 0.0;

const int MAX_STEPS = 70;
const float MAX_DIST = 1000.0;
const float MIN_DIST = 0.0001;

const vec3 spPos = vec3(0, 0, 0);
const float spRad = 0.5;

float sensitivity = 3.;

float Scale = 1.7;
vec3 Offset = vec3(-1, -1, -1);



float getDist(vec3 z, in mat3 rot)
{
	float totalScale = 1.0;
	for (int i = 0; i < uIters; i++)
	{
		z = abs(z);
		z *= Scale;
		z += Offset;
		totalScale *= Scale;
		z = rot * z;
	}

	return length(z) / totalScale - 0.1;
}



float rayMarch(vec3 ro, vec3 rd, int samples, out int it, in mat3 rot)
{
	float dO = 0.0;

	bool flag = false;
    for (int i = 0; i < samples; i++)
    {
        vec3 p = ro + rd * dO;
        float ds = getDist(p, rot);
        dO += ds;
        if (dO > MAX_DIST || ds < MIN_DIST) {
			it = i;
			flag = true;
			break;
		}
    }
	if (!flag)
    	it = samples;

    return dO;
}

/*vec3 getNormal(vec3 p)
{
    const float e = 0.005;
    float d = getDist(p);
    vec3 v = d - vec3(
        getDist(vec3(p.x - e,	p.y,		p.z)),
        getDist(vec3(p.x,		p.y - e,	p.z)),
        getDist(vec3(p.x,		p.y,		p.z - e))
    );
	return normalize(v);
}

float getLight(vec3 p)
{
    vec3 lightPos = vec3(0, 4, 5) + vec3(cos(iTime), 0, sin(iTime)) * 2.0;
    vec3 lv = normalize(vec3(-1, 1, -1));
    vec3 norm = getNormal(p);

    float res = max(0.0, dot(lv, norm));

    float d = 0;//rayMarch(p + norm * MIN_DIST * 2.0, lv, 500);
    float td = length(lightPos - p);
    if (d < td)
    	res *= d/td;

    return res;
}*/

mat3 rotationY( in float angle ) {
	return mat3(	cos(angle),		0,		sin(angle),
			 				0,		1.0,			 0,
					-sin(angle),	0,		cos(angle));
}

mat3 rotationX( in float angle ) {
	return mat3(	1.0,		0,			0,
			 		0, 	cos(angle),	-sin(angle),
					0, 	sin(angle),	 cos(angle));
}


void main()
{
		vec2 uv = (gl_FragCoord.xy-0.5*uResolution.xy)/uResolution.y;
		vec2 mpos = uMousePos.xy / uResolution.y;

    mat3 rotY = rotationY(-mpos.x * sensitivity);
    mat3 rotX = rotationX(mpos.y * sensitivity);

    vec3 ro = rotY * rotX * vec3(0, 0, -5.5);
    vec3 rd = rotY * rotX * normalize(vec3(uv.x, uv.y, uZoom));

		mat3 rot = mat3(1);
		rot = rotationX(uAlpha) * rot;
		rot = rotationY(uBeta) * rot;

		int it = 0;
    float d = rayMarch(ro, rd, MAX_STEPS, it, rot);
    vec3 p = ro + rd * d;

		float c = 1.0 - float(it) / float(MAX_STEPS);
		if (it == 0)
			c = 0.0;

		vec3 col = vec3(c);
    //vec3 col = getNormal(p);
    FragColor = vec4(col, 1.0);
}
