from polar2DAdapter import Polar2DAdapter, IPolar2D
from polar2DInheritance import Polarinheritance2D
from vector2D import IVector, Vector2D
from vector3DDecorator import Vector3DDecorator
from vector3DInheritance import Vector3DInheritance

def run():
    vector2D_1 = Polar2DAdapter(Vector2D(3, 5))
    vector3DDecorator = Vector3DDecorator(3, 5, 15)
    vector3DIngeritance = Vector3DInheritance(8, 18, 3)

    print("------------------------------\n      Cartesian Coordinates\n------------------------------")
    print(f"Vector 2D:\t\t\t{vector2D_1.getComponents()}")
    print(f"Vector 3D Decorator:\t\t{vector3DDecorator.getComponents()}")
    print(f"Vector 3D Inheritance:\t\t{vector3DIngeritance.getComponents()}")

    print("\n------------------------------\n      Polar Coordinates\n------------------------------")
    print(f"Vector 2D:\t\t\t[{round(vector2D_1.abs(), 2)}, {vector2D_1.getAngle()}]")
    print(f"Vector 3D Decorator:\t\t{vector3DDecorator.getPolars()}")
    print(f"Vector 3D Inheritance:\t\t{vector3DIngeritance.getPolars()}")

    print("\n------------------------------\n      Scalar Product\n------------------------------")
    print(f"Vector 2D and Vector 2D:\t\t\t\t{vector2D_1.cdot(vector2D_1)}")
    print(f"Vector 2D and Vector 3D Inheritance:\t\t\t{vector2D_1.cdot(vector3DIngeritance)}")
    print(f"Vector 2D and Vector 3D Decorator:\t\t\t{vector2D_1.cdot(vector3DDecorator)}")
    print(f"Vector 3D Inheritance and Vector 3D Decorator:\t\t{vector3DIngeritance.cdot(vector3DDecorator)}")
    print(f"Vector 3D Inheritance and Vector 3D Inheritance:\t{vector3DIngeritance.cdot(vector3DIngeritance)}")
    print(f"Vector 3D Decorator and Vector 3D Decorator:\t\t{vector3DDecorator.cdot(vector3DDecorator)}")

    print("\n------------------------------\n      Vector Product\n------------------------------")
    print(f"Vector 3D Inheritance and Vector 2D:\t\t\t{vector3DIngeritance.cross(vector2D_1).getComponents()}")
    print(f"Vector 3D Decorator and Vector 2D:\t\t\t{vector3DDecorator.cross(vector2D_1).getComponents()}")
    print(f"Vector 3D Inheritance and Vector 3D Decorator:\t\t{vector3DIngeritance.cross(vector3DDecorator).getComponents()}")
    print(f"Vector 3D Decorator and Vector 3D Inheritance:\t\t{vector3DDecorator.cross(vector3DIngeritance).getComponents()}")
    print("\n")

if __name__ == "__main__":
    run()