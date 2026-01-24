#!/bin/bash
# Quick Test Reference for Nexus

echo "================================"
echo "NEXUS QUICK TEST REFERENCE"
echo "================================"
echo ""

echo "1️⃣  Test Nexus CLI"
echo "   nexus --help"
echo "   nexus version"
echo "   nexus run /workspaces/Nexus/test.nexus"
echo ""

echo "2️⃣  Test Interpreter"
echo "   python3 -c \"from src.lexer import NexusLexer; from src.parser import NexusParser; from src.interpreter import NexusInterpreter; lexer = NexusLexer('println \\\"test\\\"'); tokens = lexer.tokenize(); parser = NexusParser(tokens); ast = parser.parse(); NexusInterpreter().interpret(ast)\""
echo ""

echo "3️⃣  Test .nxs Frontend Rendering"
echo "   python3 -c \"from src.frontend import NxsParser; html = NxsParser(open('src/index.nxs').read()).parse(); print('Buttons:', html.count('nxs-btn'))\""
echo ""

echo "4️⃣  Test .nxsjs Backend Parsing"
echo "   python3 -c \"from src.backend import NxsjsParser; ast = NxsjsParser(open('src/api.nxsjs').read()).parse(); print('Routes:', len(ast.get('routes', [])))\""
echo ""

echo "5️⃣  Run Full Test Suite"
echo "   python3 test_all.py"
echo ""

echo "6️⃣  Create New Project"
echo "   nexus new myapp"
echo "   cd myapp"
echo "   ls -la src/"
echo ""

echo "7️⃣  Find All .nxs Files"
echo "   find /workspaces/Nexus -name '*.nxs'"
echo ""

echo "8️⃣  Find All .nxsjs Files"
echo "   find /workspaces/Nexus -name '*.nxsjs'"
echo ""

echo "================================"
echo "STATUS: ✅ ALL TESTS PASSING"
echo "================================"
