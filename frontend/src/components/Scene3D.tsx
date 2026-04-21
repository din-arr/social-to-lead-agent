import { Suspense, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { useGLTF, Float, Environment, ContactShadows, MeshDistortMaterial } from "@react-three/drei";
import type { Group, Mesh } from "three";
import helmetUrl from "@/assets/models/helmet.glb?url";
import robotUrl from "@/assets/models/robot.glb?url";

function Helmet(props: { position?: [number, number, number]; scale?: number }) {
  const { scene } = useGLTF(helmetUrl);
  const ref = useRef<Group>(null);
  useFrame((_, dt) => {
    if (ref.current) ref.current.rotation.y += dt * 0.25;
  });
  return (
    <group ref={ref} position={props.position ?? [0, 0, 0]} scale={props.scale ?? 1}>
      <primitive object={scene} />
    </group>
  );
}

function BlobShape(props: { position: [number, number, number]; color: string; speed?: number }) {
  const ref = useRef<Mesh>(null);
  useFrame((state) => {
    if (!ref.current) return;
    ref.current.rotation.x = state.clock.elapsedTime * 0.2;
    ref.current.rotation.y = state.clock.elapsedTime * 0.15;
  });
  return (
    <Float speed={props.speed ?? 1.4} rotationIntensity={0.6} floatIntensity={1.4}>
      <mesh ref={ref} position={props.position}>
        <icosahedronGeometry args={[1, 6]} />
        <MeshDistortMaterial
          color={props.color}
          distort={0.45}
          speed={2}
          roughness={0.15}
          metalness={0.6}
        />
      </mesh>
    </Float>
  );
}

function TorusKnot(props: { position: [number, number, number] }) {
  const ref = useRef<Mesh>(null);
  useFrame((_, dt) => {
    if (ref.current) {
      ref.current.rotation.x += dt * 0.3;
      ref.current.rotation.y += dt * 0.2;
    }
  });
  return (
    <Float speed={2} rotationIntensity={1} floatIntensity={2}>
      <mesh ref={ref} position={props.position} scale={0.55}>
        <torusKnotGeometry args={[1, 0.3, 220, 32]} />
        <meshStandardMaterial color="#ff7a4d" metalness={0.85} roughness={0.2} />
      </mesh>
    </Float>
  );
}

export function HeroScene() {
  return (
    <Canvas
      dpr={[1, 2]}
      camera={{ position: [0, 0, 6], fov: 45 }}
      gl={{ antialias: true, alpha: true }}
    >
      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 5, 5]} intensity={1.2} />
      <pointLight position={[-5, -3, -2]} intensity={1.5} color="#c8ff3d" />
      <Suspense fallback={null}>
        <Float speed={1.2} rotationIntensity={0.4} floatIntensity={1.2}>
          <Helmet position={[0, -0.2, 0]} scale={1.7} />
        </Float>
        <BlobShape position={[-3.2, 1.4, -1]} color="#c8ff3d" speed={1.2} />
        <BlobShape position={[3.2, -1.2, -1.5]} color="#7ad7ff" speed={1.6} />
        <TorusKnot position={[2.6, 1.8, -0.5]} />
        <Environment preset="city" />
        <ContactShadows position={[0, -1.6, 0]} opacity={0.4} scale={10} blur={2.4} far={3} />
      </Suspense>
    </Canvas>
  );
}

export function RobotScene() {
  return (
    <Canvas dpr={[1, 2]} camera={{ position: [0, 1, 4], fov: 40 }} gl={{ alpha: true }}>
      <ambientLight intensity={0.6} />
      <directionalLight position={[3, 4, 2]} intensity={1.1} />
      <pointLight position={[-4, 2, -2]} intensity={2} color="#c8ff3d" />
      <Suspense fallback={null}>
        <Float speed={1.4} rotationIntensity={0.3} floatIntensity={0.8}>
          <RobotModel />
        </Float>
        <Environment preset="studio" />
      </Suspense>
    </Canvas>
  );
}

function RobotModel() {
  const { scene } = useGLTF(robotUrl);
  const ref = useRef<Group>(null);
  useFrame((_, dt) => {
    if (ref.current) ref.current.rotation.y += dt * 0.4;
  });
  return (
    <group ref={ref} position={[0, -0.8, 0]} scale={1.2}>
      <primitive object={scene} />
    </group>
  );
}

useGLTF.preload(helmetUrl);
useGLTF.preload(robotUrl);

