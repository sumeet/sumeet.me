func compileDeclaration(d Declaration) string {
    {
        matchExpr := d
        if binding, ok := matchExpr.(DeclarationEnum); ok {
            _ = binding
            e := binding.Value
            _ = e
            {
                return compileEnum(e)
            }

        } else if binding, ok := matchExpr.(DeclarationImport); ok {
            _ = binding
            imp := binding.Value
            _ = imp
            {
                return compileImport(imp)
            }

        } else if binding, ok := matchExpr.(DeclarationStruct); ok {
            _ = binding
            s := binding.Value
            _ = s
            {
                return compileStruct(s)
            }

        } else if binding, ok := matchExpr.(DeclarationFunction); ok {
            _ = binding
            f := binding.Value
            _ = f
            {
                return compileFunction(f)
            }

        }
    }
}
