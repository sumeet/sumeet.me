type Declaration interface {
    _implementsDeclaration()
}
type DeclarationEnum struct {
    Value Enum
}

func (_ DeclarationEnum) _implementsDeclaration() {}

type DeclarationImport struct {
    Value Import
}

func (_ DeclarationImport) _implementsDeclaration() {}

type DeclarationStruct struct {
    Value Struct
}

func (_ DeclarationStruct) _implementsDeclaration() {}

type DeclarationFunction struct {
    Value Function
}

func (_ DeclarationFunction) _implementsDeclaration() {}
